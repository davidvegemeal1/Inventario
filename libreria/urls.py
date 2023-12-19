from django.urls import path
from . import views


urlpatterns=[
    path('', views.home, name= "home"),
    path('iniciar/', views.iniciar, name= "iniciar"),
     path('somos/', views.somos, name= "somos"),   
    path('principal/', views.principal, name= "principal"), 
    path('crear/', views.crear, name= "crear"), 
    path('editar/<int:pan_id>/', views.editar, name= "editar"),
    path('salir/',views.salir, name='salir' ), 
    path('borrar/<int:pan_id>/', views.delete_pan, name='delete_pan'),
    path('generar_pdf/', views.generar_pdf, name='generar_pdf'),

]