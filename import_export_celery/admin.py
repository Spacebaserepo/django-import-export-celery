# Copyright (C) 2019 o.s. Auto*Mat
from importlib import import_module

from django import forms
from django.conf import settings
from django.contrib import admin
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

from . import admin_actions, get_job_models


ImportJob, ExportJob = get_job_models()


class JobWithStatusMixin:
    @admin.display(description=_("Job status info"))
    def job_status_info(self, obj):
        job_status = cache.get(self.direction + "_job_status_%s" % obj.pk)
        if job_status:
            return job_status
        else:
            return obj.job_status


class ImportJobForm(forms.ModelForm):
    model = forms.ChoiceField(label=_("Name of model to import to"))

    class Meta:
        model = ImportJob
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["model"].choices = [
            (x, x) for x in getattr(settings, "IMPORT_EXPORT_CELERY_MODELS", {}).keys()
        ]
        self.fields["format"].widget = forms.Select(
            choices=self.instance.get_format_choices()
        )


import_form_path = getattr(settings, 'IMPORT_EXPORT_CELERY_IMPORT_JOB_ADMIN_FORM', None)
if import_form_path:
    module_name, class_name = import_form_path.rsplit('.', 1)
    m = import_module(module_name)
    ImportJobForm = getattr(m, class_name)


class ImportJobAdmin(JobWithStatusMixin, admin.ModelAdmin):
    direction = "import"
    form = ImportJobForm
    list_display = (
        "model",
        "job_status_info",
        "file",
        "change_summary",
        "imported",
        "author",
        "updated_by",
    )
    readonly_fields = (
        "job_status_info",
        "change_summary",
        "imported",
        "errors",
        "author",
        "updated_by",
        "processing_initiated",
    )
    exclude = ("job_status",)

    list_filter = ("model", "imported")

    actions = (
        admin_actions.run_import_job_action,
        admin_actions.run_import_job_action_dry,
    )


class ExportJobForm(forms.ModelForm):
    class Meta:
        model = ExportJob
        exclude = ("site_of_origin",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["resource"].widget = forms.Select(
            choices=self.instance.get_resource_choices()
        )
        self.fields["format"].widget = forms.Select(
            choices=self.instance.get_format_choices()
        )


export_form_path = getattr(settings, 'IMPORT_EXPORT_CELERY_EXPORT_JOB_ADMIN_FORM', None)
if export_form_path:
    module_name, class_name = export_form_path.rsplit('.', 1)
    m = import_module(module_name)
    ExportJobForm = getattr(m, class_name)


class ExportJobAdmin(JobWithStatusMixin, admin.ModelAdmin):
    direction = "export"
    form = ExportJobForm
    list_display = (
        "model",
        "app_label",
        "file",
        "job_status_info",
        "author",
        "updated_by",
    )
    readonly_fields = (
        "job_status_info",
        "author",
        "updated_by",
        "app_label",
        "model",
        "file",
        "processing_initiated",
    )
    exclude = ("job_status",)

    list_filter = ("model",)

    def has_add_permission(self, request, obj=None):
        return False

    actions = (admin_actions.run_export_job_action,)


if getattr(settings, 'IMPORT_EXPORT_CELERY_REGISTER_IMPORTJOB_MODEL', True):
    admin.site.register(ImportJob, ImportJobAdmin)

if getattr(settings, 'IMPORT_EXPORT_CELERY_REGISTER_EXPORTJOB_MODEL', True):
    admin.site.register(ExportJob, ExportJobAdmin)
