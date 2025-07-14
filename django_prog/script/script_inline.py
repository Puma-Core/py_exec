from django.contrib import admin
from django_prog.script.models import WorkflowScript


class WorkflowScriptInline(admin.TabularInline):
    model = WorkflowScript
    extra = 1
