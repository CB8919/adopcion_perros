from django.urls import path
from . import views

urlpatterns = [
    path("", views.vista_index, name="vista_index"),
    path("agregar-perro/", views.vista_agregar_perro, name="vista_agregar_perro"),
    path("registrar_user/", views.vista_registrar_user, name="vista_registrar_user"),
    path("listado-perros/", views.vista_listado_perros, name="listado_perros"),
    path("eliminar_perro/", views.vista_eliminar_perro, name="vista_eliminar_perro"),
    path("confirmar_adopcion/", views.vista_confirmar_adopcion, name="vista_confirmar_adopcion"),
    path("postular_perro/", views.vista_postular_perro, name="vista_postular_perro"),
    path("preferencia_perros/", views.vista_preferencia_perros, name="vista_preferencia_perros"),
    path("salir/", views.vista_salir, name="vista_salir"),
    
]