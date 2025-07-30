from typing import Any, Callable, Self
from django.contrib import admin
from django.urls import path
    

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
    change_form_template = 'admin/common/change_form.html'
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

    def get_urls(self: Self) -> Any:
        urls = super().get_urls() + self.build_btn_paths()
        return urls

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context["btn_methods"] = self.get_btn_methods()
        return super().change_view(request, object_id, form_url, extra_context)