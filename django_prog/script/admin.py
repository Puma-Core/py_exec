from django.contrib import admin
from django_prog.script.forms import ScriptForm
from django_prog.script.models import Script


@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    form = ScriptForm
