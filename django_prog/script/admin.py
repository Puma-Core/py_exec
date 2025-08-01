from django.contrib import admin
from django.shortcuts import redirect
from django_prog.common.admin import PumaAdminModel
from django_prog.script.forms import ScriptForm, WorkflowForm
from django_prog.script.models import Script, Workflow
from django_prog.script.script_inline import WorkflowScriptInline
from django.utils.safestring import mark_safe
import json

from django_prog.task.script import run_script


@admin.register(Script)
class ScriptAdmin(PumaAdminModel):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    form = ScriptForm

    def btn__run(self, request, object_id, form_url='', extra_context=None):
        script_admin = self.get_object(request, object_id)
        run_script.delay(script_code=script_admin.content)
        return redirect(request.path)

@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    form = WorkflowForm
    inlines = [WorkflowScriptInline]
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']
