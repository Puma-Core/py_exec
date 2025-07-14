from django.contrib import admin
from django.utils.safestring import mark_safe
from django_prog.script.models import WorkflowScript, Script
import json


class WorkflowScriptInline(admin.TabularInline):
    model = WorkflowScript
    extra = 1
    fields = ['script', 'script_info_display', 'order', 'is_active']
    readonly_fields = ['script_info_display']

    class Media:
        js = ('admin/js/script_info_updater.js',)

    def script_info_display(self, obj):
        # Generar datos de todos los scripts para JavaScript
        scripts = Script.objects.all()
        script_data = {}
        for script in scripts:
            script_data[str(script.id)] = {
                'name': script.name,
                'created_at': script.created_at.strftime('%Y-%m-%d'),
                'is_active': script.is_active,
                'content': script.content[:50] + "..." if len(script.content) > 50 else script.content
            }

        # Información actual
        current_info = "-"
        if obj and obj.script:
            status = "✅ Active" if obj.script.is_active else "❌ Inactive"
            created = obj.script.created_at.strftime('%Y-%m-%d')
            content_preview = obj.script.content[:50] + "..." if len(obj.script.content) > 50 else obj.script.content
            current_info = f"{status} | Created: {created}<br><small>Preview: {content_preview}</small>"
        
        # Generar un ID único para esta fila
        row_id = f"script-info-{obj.id if obj else 'new'}"
        return mark_safe(f"""
            <div id="{row_id}" class="script-info-container" data-script-data='{json.dumps(script_data)}'>
                <div class="script-info">{current_info}</div>
            </div>
        """)
    script_info_display.short_description = "Script Info"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('script')