# Copyright (C) 2019 o.s. Auto*Mat

from django.utils import timezone

from author.decorators import with_author

from django.db import models

from django.utils.translation import gettext_lazy as _

from import_export.formats.base_formats import DEFAULT_FORMATS


@with_author
class ImportJob(models.Model):
    file = models.FileField(
        verbose_name=_("File to be imported"),
        upload_to="django-import-export-celery-import-jobs",
        blank=False,
        null=False,
        max_length=255,
    )

    processing_initiated = models.DateTimeField(
        verbose_name=_("Have we started processing the file? If so when?"),
        null=True,
        blank=True,
        default=None,
    )

    imported = models.DateTimeField(
        verbose_name=_("Has the import been completed? If so when?"),
        null=True,
        blank=True,
        default=None,
    )

    format = models.CharField(
        verbose_name=_("Format of file to be imported"),
        max_length=255,
    )

    change_summary = models.FileField(
        verbose_name=_("Summary of changes made by this import"),
        upload_to="django-import-export-celery-import-change-summaries",
        blank=True,
        null=True,
    )

    errors = models.TextField(
        default="",
        blank=True,
    )

    model = models.CharField(
        verbose_name=_("Name of model to import to"),
        max_length=160,
    )

    job_status = models.CharField(
        verbose_name=_("Status of the job"),
        max_length=160,
        blank=True,
    )

    @staticmethod
    def get_format_choices():
        """returns choices of available import formats"""
        return [
            (f.CONTENT_TYPE, f().get_title())
            for f in DEFAULT_FORMATS
            if f().can_import()
        ]
