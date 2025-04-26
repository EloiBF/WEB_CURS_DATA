from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Afegir aquesta línia per a l'administrador
    path('', views.landing_page, name='landing_page'),
    path('curs/<str:curs_nom>/', views.index_curs, name='index_curs'),
    path('curs/<str:curs_nom>/exercici/<int:exercici_id>/', views.exercici, name='exercici'),
    path('contacte/',views.enviar_contacte,name='enviar_contacte'),
]

