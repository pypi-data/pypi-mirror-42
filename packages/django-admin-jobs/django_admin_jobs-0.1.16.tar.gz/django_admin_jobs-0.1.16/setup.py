from setuptools import setup, find_packages
from distutils.command.install import INSTALL_SCHEMES

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

setup(
    # Application name
    name="django_admin_jobs",

    # Version number
    version="0.1.16",

    # Application author details
    author="Dimitris Papaspyros",
    author_email="dimitris@orfium.com",

    # Packages
    packages=find_packages(),

    # Include additional files into the package
    include_package_data=True,
    package_data={
        'django_admin_jobs': [
            'templates/admin/django_admin_jobs/upload_job/change_list.html',
            'static/django-admin-jobs/js/firebase/firebase-4.2.0.min.js',
            'static/django-admin-jobs/js/firebase/firebase-listener.js',
            'static/django-admin-jobs/js/monitor.js'
        ],
    },

    # Details
    license="LICENSE",
    description="A toolset for jobs in the django admin interface.",

    # Dependent packages (distributions)
    install_requires=[
        "django",
        "python-firebase",
    ],
)
