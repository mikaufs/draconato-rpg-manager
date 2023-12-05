from django.contrib import admin
from django.urls import path, include
from manager.views import ListarInicio, ListarMCampanhas, CampanhaCreateView, TesteDashboard
from manager.views import pesquisa
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    
    path('', ListarInicio.as_view(),name='index'),
    path('minhascampanhas', ListarMCampanhas.as_view(), name='minhascampanhas'),
    path('campanha/criar', CampanhaCreateView.as_view(), name='campanha-criar'),
    path('campanha/<int:pk>', TesteDashboard.as_view(), name='dashboard'),
    path('pesquisa_campanhas', pesquisa, name='pesquisa_campanhas'),

]+ static (settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
