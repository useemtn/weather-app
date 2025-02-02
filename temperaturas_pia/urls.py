from django.contrib import admin
from django.urls import path
from django.conf.urls import include

"""

URLs para el proyecto, hay que incluir las urls de la app

"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('temperaturas_app.urls')),
]
