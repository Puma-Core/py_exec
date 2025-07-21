from ninja import Router, Schema
from ninja.security import django_auth
from django.shortcuts import get_object_or_404
from django.http import Http404
from typing import Optional
from .models import Script


class ScriptSchema(Schema):
    id: int
    name: str
    created_at: str
    updated_at: str
    is_active: bool
    order: int


class ErrorSchema(Schema):
    error: str
    detail: Optional[str] = None


routes = Router(
    tags=["scripts"],
    auth=django_auth
)


@routes.get("/{script_id}", response={200: ScriptSchema, 404: ErrorSchema})
def get_script(request, script_id: int):
    """
    Get a script by ID.
    Requires Django authentication.
    """
    try:
        script = get_object_or_404(Script, id=script_id)
        return {
            "id": script.id,
            "name": script.name,
            "content": script.content,
            "created_at": script.created_at.isoformat(),
            "updated_at": script.updated_at.isoformat(),
            "is_active": script.is_active,
            "order": script.order
        }
    except Http404:
        return 404, {
            "error": "Script not found",
            "detail": f"Script with ID {script_id} does not exist"
        }


@routes.get("", response=list[ScriptSchema])
def list_scripts(request):
    """
    List all scripts.
    Requires Django authentication.
    """
    scripts = Script.objects.all()
    return [
        {
            "id": script.id,
            "name": script.name,
            "content": script.content,
            "created_at": script.created_at.isoformat(),
            "updated_at": script.updated_at.isoformat(),
            "is_active": script.is_active,
            "order": script.order
        }
        for script in scripts
    ]
