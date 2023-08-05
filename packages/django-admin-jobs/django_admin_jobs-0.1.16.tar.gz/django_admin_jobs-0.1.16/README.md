# django\_admin\_jobs

## Purpose
This django app provides you with an interface & management command for interactive admin tasks.

## Instructions

1. Add `django_admin_jobs` to your project requirements:
pip install git+https://bitbucket.org/hexacorp-ltd/django_admin_jobs.git

2. Include the package `django_admin_jobs` in the `INSTALLED_APPS` setting.

3. Create an application on Firebase and then add the following to your settings:

```python
FIREBASE = {
    'API_KEY': '<YourApiKey>',
    'DOMAIN': '<YourAppId>.firebaseio.com',
    'NAME': 'https://<YourAppId>.firebaseio.com',
    'PROJECT_ID': '<YourAppId>',
    'SENDER_ID': '<YourProjectId>',
}
```

4. Run migrations
`python manage.py migrate`

5. Implement your model by extending the `django_admin_jobs.models.UploadJob` model and implement the `_process` method:

```python
from django_admin_jobs.models import UploadJob, UploadJobProgress
from django.db.models import IntegerField
import time

class SleeperJob(UploadJob):
    """
    A job that sleeps for a number of seconds
    """
    counter = IntegerField()

    def save(self, *args, **kwargs):
        self.upload_type = 'SleeperJob'
        super(AssetUploadJob, self).save(*args, **kwargs)

    def _process(self):

        for idx in range(self.counter):

            # yield progress
            yield UploadJobProgress(
                status='RUNNING',
                message='Taking my #%d nap...' % (idx + 1)
            )

            # perform the actual task
            time.sleep(1)

        # if you want to raise an error
        yield UploadJobProgress(
            status='FAILED',
            message='Someone woke me up...'
        )

        # when task finishes
        yield UploadJobProgress(
            status='FINISHED',
            message='Finished taking naps!'
        )
```

6. Register your model in the admin by using or extending the `django_admin_jobs.admin.UploadJobAdmin` class:

```python
# in your admin.py

from django_admin_jobs.admin import UploadJobAdmin
from django.contrib import admin

admin.site.register(MyCustomAdminJob, UploadJobAdmin)
```

7. Once you create & apply migrations for your custom model(s) you can create jobs through the django admin.
Make sure to schedule or manually run the following command to process them.
Use the timeout flag to specify for how long the command should listen for new jobs (in minutes):

`python manage.py run_upload_jobs --timeout=10  # runs for 10 minutes`
