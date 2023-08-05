import time
from django.core.management import BaseCommand, CommandError
from django.utils.timezone import now

from django_admin_jobs.models import UploadJob
from django_admin_jobs.task_pool import TaskPool


def process_job(job):
    job_id = str(job.pk)[:6]
    print('Picked job #%s...' % job_id)

    # process it
    job.process()

    print('Job #%s -> %s' % (job_id, job.get_status_display()))


class Command(BaseCommand):
    help = 'Process submitted upload jobs'

    def add_arguments(self, parser):
        parser.add_argument(
            "-t",
            "--timeout",
            dest="timeout",
            action='store',
            default=None,
            help="Minutes after which the job exits (never by default)."
        )
        parser.add_argument(
            "-w",
            "--workers",
            dest="workers",
            action='store',
            default=1,
            help="Number of workers (defaults to 1)."
        )

    def handle(self, *args, **options):
        # read workers
        try:
            workers = int(options['workers'])

            if workers <= 0:
                raise ValueError()
        except ValueError:
            raise CommandError('Invalid workers - must be a positive integer.')

        # read timeout
        timeout = options['timeout']

        if timeout is not None:
            try:
                timeout = int(timeout)

                if timeout <= 0:
                    raise ValueError()
            except ValueError:
                raise CommandError('Invalid timeout - must be a positive integer or not be provided at all.')

        started_at = now()

        task_pool = TaskPool(workers=workers)

        while True:
            if not task_pool.is_full():
                try:
                    # fetch a job
                    job = UploadJob.objects.filter(status='SUBMITTED')[0].item

                    # add to pool
                    task_pool.add_task(process_job, (job, ))

                except IndexError:
                    pass

            # wait for a while
            time.sleep(2)

            # check if timeout is exceeded
            if timeout is not None and ((now() - started_at).seconds >= timeout * 60):
                self.stdout.write('Timeout reached')

                return
