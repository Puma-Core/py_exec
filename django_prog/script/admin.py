from django.contrib import admin
from django_prog.script.forms import ScriptForm, WorkflowForm
from django_prog.script.models import Script, Workflow
from django_prog.script.script_inline import WorkflowScriptInline
from django.utils.safestring import mark_safe
import json


@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    form = ScriptForm


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    form = WorkflowForm
    inlines = [WorkflowScriptInline]
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']
