from django.urls import path
from . import views
"""	

Endpoints para las funciones de la app

"""	
urlpatterns = [
    path('', views.index, name='index'),  
    path('mostrar_temperatura/', views.mostrar_temperatura, name='mostrar_temperatura'),
    path('borrar_bd/', views.borrar_bd, name='borrar_bd'),
    path('insertar_paises/', views.insertar_paises, name='insertar_paises'),
    path('insertar_fronteras/', views.insertar_fronteras, name='insertar_fronteras'),
    path('insertar_temperaturas/', views.insertar_temperaturas, name='insertar_temperaturas'),
    path('obtener_temperaturas/', views.obtener_temperaturas, name='obtener_temperaturas'),
    path('mostrar_temperatura/', views.mostrar_temperatura, name='mostrar_temperatura'),
]