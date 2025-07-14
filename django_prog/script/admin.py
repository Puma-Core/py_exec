from django.contrib import admin
from django.db import models
from django_prog.script.forms import ScriptForm, WorkflowForm
from django_prog.script.models import Script, Workflow, WorkflowScript


@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    form = ScriptForm


class WorkflowScriptInline(admin.StackedInline):
    model = WorkflowScript
    extra = 1


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    form = WorkflowForm
    inlines = [WorkflowScriptInline]
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
