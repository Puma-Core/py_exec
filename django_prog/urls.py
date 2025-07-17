from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from ninja import NinjaAPI
from django_prog.script.api import routes as routes_script

api = NinjaAPI()

api.add_router('/scripts/', routes_script)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
] + staticfiles_urlpatterns()
