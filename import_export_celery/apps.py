from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ImportExportCeleryConfig(AppConfig):
    name = "import_export_celery"
    verbose_name = _("Import Export Celery")

    def ready(self):
        from import_export_celery import signals

