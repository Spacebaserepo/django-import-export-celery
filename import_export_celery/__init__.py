from django.conf import settings


def get_job_models():
    from django.apps import apps
    from .models import ImportJob as import_job_model
    from .models import ExportJob as export_job_model

    importjob_model_path = getattr(settings, 'IMPORT_EXPORT_CELERY_IMPORT_JOB_MODEL', None)
    if importjob_model_path:
        import_job_model = apps.get_model(*importjob_model_path.split('.'))

    exportjob_model_path = getattr(settings, 'IMPORT_EXPORT_CELERY_EXPORT_JOB_MODEL', None)
    if exportjob_model_path:
        export_job_model = apps.get_model(*exportjob_model_path.split('.'))

    return import_job_model, export_job_model
