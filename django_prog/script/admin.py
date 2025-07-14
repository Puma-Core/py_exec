from django.contrib import admin
from django_prog.script.forms import ScriptForm, WorkflowForm
from django_prog.script.models import Script, Workflow, WorkflowScript
from django_prog.script.script_inline import WorkflowScriptInline


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
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
