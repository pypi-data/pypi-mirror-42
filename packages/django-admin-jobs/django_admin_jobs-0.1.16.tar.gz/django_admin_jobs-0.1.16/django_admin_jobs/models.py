# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta

import sys
import uuid
import threading
import traceback

from django.db import transaction
from django.db.models import *
from django.db.transaction import TransactionManagementError
from django.utils.timezone import now
from firebase import firebase

from django.conf import settings


class UploadJobProgress(object):
    """
    An object that is yielded by the _process method
    of all classes that implement AbstractUploadJob
    and reports the current status back
    """
    VALID_STATUSES = ['SUBMITTED', 'STARTED', 'RUNNING', 'FINISHED', 'FAILED']

    def __init__(self, status, message):
        if status not in self.VALID_STATUSES:
            raise ValueError('`status` must be one of %s' % ','.join(self.VALID_STATUSES))

        self.status = status
        self.message = message
        self.reported_at = now()


def run_write_progress(job, progress):
    job._write_progress(progress)


class FailedProcessError(ValueError):

    def __init__(self, progress):
        self.progress = progress


class UploadJob(Model):
    """
    Basic setup for all upload jobs
    """
    id = UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now_add=True)
    started = DateTimeField(blank=True, null=True, default=None)
    finished = DateTimeField(blank=True, null=True, default=None)
    info = TextField(blank=True, null=True, default=None)
    upload_type = CharField(max_length=32, blank=False)
    status = CharField(max_length=32, choices=(
        ('SUBMITTED', 'Submitted'),
        ('STARTED', 'Started'),
        ('FINISHED', 'Finished'),
        ('FAILED', 'Failed'),
    ), default='SUBMITTED')

    transactional = True

    def write_progress(self, progress):
        try:
            self.last_reported_progress
        except AttributeError:
            self.last_reported_progress = None

        # only actually write the progress periodically
        if (self.last_reported_progress is None) or \
                (progress.status != 'RUNNING') or \
                (progress.reported_at - self.last_reported_progress.reported_at
                     >= timedelta(seconds=1)):
            self.last_reported_progress = progress

            # update progress on firebase
            self._write_progress(progress)

    @staticmethod
    def time_format():
        return '%Y-%m-%d %H:%M:%S'

    def _write_progress(self, progress):
        progress_doc = {
            'status': progress.status.title(),
            'started': self.started.strftime(self.time_format()) if self.started else None,
            'finished': self.finished.strftime(self.time_format()) if self.finished else None,
            'message': progress.message,
        }

        try:
            if settings.TESTING:
                self._progress = progress_doc
                return
        except AttributeError:
            pass

        # write progress to firebase
        if 'CREDENTIALS' in settings.FIREBASE:
            auth = firebase.FirebaseAuthentication(settings.FIREBASE['API_KEY'], 'admin')
            app = firebase.FirebaseApplication(settings.FIREBASE['NAME'], auth)
        else:
            app = firebase.FirebaseApplication(settings.FIREBASE['NAME'])

        # don't fail on firebase error if running
        try:
            app.patch('uploads/%s' % str(self.pk), progress_doc)
        except:
            if progress.status != 'RUNNING':
                raise

        # also push to additional key (if any)
        self.extra_send_data(app, progress_doc)

    def extra_send_data(self, app, data):
        return

    def _read_state_from_firebase(self):

        try:
            if settings.TESTING:
                return self._progress
        except AttributeError:
            pass

        # write progress to firebase
        app = firebase.FirebaseApplication(settings.FIREBASE['NAME'])
        result = app.get('uploads', str(self.pk))

        for time_key in ['started', 'finished']:
            if time_key in result:
                try:
                    result[time_key] = datetime.strptime(result[time_key], self.time_format())
                except ValueError:
                    pass

        return result

    def restart(self):
        self.started = None
        self.finished = None
        self.status = 'SUBMITTED'
        self.info = ''
        self.save()

        self.write_progress(UploadJobProgress(status=self.status, message=self.info))

    def mark_as_started(self):
        self.started = now()
        self.finished = None
        self.status = 'STARTED'
        self.info = 'Started job'
        self.save()

        self.write_progress(UploadJobProgress(status=self.status, message=self.info))

    def mark_as_failed(self, exc=None):
        self.status = 'FAILED'
        self.info = 'Processing error: %s' % (str(exc) if exc is not None else '')
        self.save()

        try:
            self.write_progress(UploadJobProgress(status=self.status, message=self.info))
        except:
            pass

    @property
    def item(self):
        result = getattr(self, self.upload_type.lower(), None)

        if result is None:
            raise ValueError('Invalid upload job type: %s' % self.upload_type)

        return result

    def run_process_iterator(self):
        final_progress = None
        for progress in self._process():

            # check if done
            if progress.status in ['FINISHED', 'FAILED']:
                final_progress = progress

                if progress.status == 'FAILED':
                    raise FailedProcessError(progress=final_progress)

                break
            else:
                self.write_progress(progress)

        return final_progress

    def process(self):

        if self.status == 'FINISHED':
            return

        # mark as started
        self.mark_as_started()

        try:
            # process atomically in order to rollback in case of error/restart
            final_progress = None

            try:
                if self.transactional:
                    with transaction.atomic():
                        final_progress = self.run_process_iterator()
                else:
                    final_progress = self.run_process_iterator()

            except FailedProcessError as e:
                # we're just raising the exception to ensure nothing was saved
                final_progress = e.progress

            if final_progress:
                self.status = final_progress.status
                self.info = final_progress.message
                self.finished = now()
                self.save()

                self.write_progress(final_progress)

        except TransactionManagementError as e:
            pass
        except (KeyboardInterrupt, SystemError, SystemExit) as e:
            self.mark_as_failed(e)

            sys.exit(0)
        except Exception as e:
            traceback.print_exc()

            self.mark_as_failed(e)

    def _process(self):
        # Implement as an iterator that yields UploadJobProgress objects until it finishes/fails
        raise NotImplementedError('')
