from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Afegir aquesta línia per a l'administrador
    path('', views.landing_page, name='landing_page'),
    path('curs/<str:curs_nom>/', views.index_curs, name='index_curs'),
    path('curs/<str:curs_nom>/capitol/<int:capitol_num>/exercici/<int:exercici_num>/', views.exercici, name='exercici'),
    path('curs/<str:curs_nom>/capitol/<int:capitol_num>/cas-practic/', views.cas_practic, name='cas_practic'),
    path('contacte/',views.enviar_contacte,name='enviar_contacte'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

