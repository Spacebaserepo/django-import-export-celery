from django.db import transaction
from django.db.models.signals import post_save
from django.utils import timezone

from import_export_celery import get_job_models
from import_export_celery.tasks import run_import_job, run_export_job


ImportJob, ExportJob = get_job_models()


def importjob_post_save(sender, instance, **kwargs):
    if not instance.processing_initiated:
        instance.processing_initiated = timezone.now()
        instance.save()
        transaction.on_commit(lambda: run_import_job.delay(instance.pk, dry_run=True))


def exportjob_post_save(sender, instance, **kwargs):
    if instance.resource and not instance.processing_initiated:
        instance.processing_initiated = timezone.now()
        instance.save()
        transaction.on_commit(lambda: run_export_job.delay(instance.pk))


post_save.connect(importjob_post_save, ImportJob)
post_save.connect(exportjob_post_save, ExportJob)
