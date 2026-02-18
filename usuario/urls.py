from django.urls import path
from . import views

urlpatterns = [
    
    path('login/', views.login_usuario, name='login'),
    path('perfil/', views.perfil, name='perfil'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('inicio/', views.inicio, name='inicio'),
    path('registro/', views.registro_usuario, name='registro_usuario'),

    # CRUD inventario
    path("inventario/", views.inventario_lista, name="inventario_lista"),
    path("crear/", views.inventario_crear, name="inventario_crear"),
    path("editar/<int:id>/", views.inventario_editar, name="inventario_editar"),
    path("eliminar/<int:id>/", views.inventario_eliminar, name="inventario_eliminar"),

]
