# coding=utf-8
from django.contrib import admin
from formed.models import FormDefinition
from formed.admin import FormDefinitionAdmin, FormSubmissionNotificationInline
from cms.admin.placeholderadmin import PlaceholderAdminMixin
from .models import FormPluginSubmissionNotification


class FormPluginSubmissionNotificationInline(FormSubmissionNotificationInline):
    model = FormPluginSubmissionNotification


class CMSFormDefinitionAdmin(PlaceholderAdminMixin, FormDefinitionAdmin):
    pass

admin.site.unregister(FormDefinition)
admin.site.register(FormDefinition, CMSFormDefinitionAdmin)
