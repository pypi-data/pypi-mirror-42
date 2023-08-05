# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.safestring import mark_safe

from .models import *

from django.contrib import admin


class UploadJobAdmin(admin.ModelAdmin):
    list_display = ('code', 'created', 'start_time', 'end_time', 'status', 'details', )
    list_filter = ('status', )
    readonly_fields = ('id', 'started', 'finished', 'status', 'info', 'upload_type', )
    change_list_template = 'admin/django_admin_jobs/upload_job/change_list.html'
    ordering = ('-created', )
    actions = ['restart_action', ]

    def restart_action(self, request, queryset):
        cnt = queryset.count()

        for job in queryset:
            job.restart()

        self.message_user(request, "%s job(s) restarted." % cnt)

    restart_action.short_description = "Restart selected job(s)"

    def start_time(self, obj):
        return obj.started.strftime('%Y-%m-%d %H:%M:%S') if obj.started else '-'

    def end_time(self, obj):
        return obj.finished.strftime('%Y-%m-%d %H:%M:%S') if obj.finished else '-'

    def code(self, obj):
        return mark_safe('<div class="upload-job-code%s" data-jobid="%s">%s</div>' % (
            ' finished' if obj.status == 'FINISHED' else '', str(obj.pk), str(obj.pk)[:6]
        ))

    def details(self, obj):
        return obj.info

