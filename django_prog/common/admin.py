from typing import Any, Callable, Self
from django.contrib import admin
from django.urls import path
from django_prog.common.func import replace_prefix_list    

list_routes = [
    path(
        "method/<str:pk>/",
        name="method_detail",
        view=lambda request, pk: f"Method detail for {pk}"
    )
]

class PumaAdminModel(admin.ModelAdmin):
    """
    Base model for Puma Admin with common fields.
    """
    _prefix_btn_md = "btn__"

    def get_btn_methods(self) -> list[str]:
        """
        Extract all methods of the instance whose names start with 'btn__'.
        """
        methods = [
            f for f in dir(self) if f.startswith(self._prefix_btn_md)
        ]
        return methods

    def build_btn_paths(self) -> list[Callable]:
        """
        Build URL paths for all methods of the instance whose names start with 'btn__'.
        """
        methods = self.get_btn_methods()
        url_paths = [
            path(
                f"{method}/",
                name=f"admin:{method}",
                view=lambda request, pk: f"Button method {method} called"
            ) for method in methods
        ]
        return url_paths

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context["btn_methods"] = replace_prefix_list(
            self.get_btn_methods(),
            self._prefix_btn_md
        )
        return super().change_view(request, object_id, form_url, extra_context)

    def get_urls(self: Self) -> Any:
        urls = super().get_urls() + self.build_btn_paths()
        return urls
    
    def response_change(self, request, obj):
        """
        Override to handle custom button actions.
        """

        method_name = next(
            (
                k for k in request.POST.keys()
                if k.startswith(self._prefix_btn_md)
            ),
            None
        )

        if method_name and hasattr(self, method_name):
            return getattr(self, method_name)(request, obj.pk)
        return super().response_change(request, obj)
