from django.contrib import admin
from django.urls import path, include
from manager.views import ListarInicio, ListarMCampanhas, CampanhaCreate, Dashboard, ListarPainelADM, ListarPainelCampanhasADM
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    
    path('', ListarInicio.as_view(),name='index'),
    path('minhascampanhas', ListarMCampanhas.as_view(), name='minhascampanhas'),
    path('campanha/criar', CampanhaCreate.as_view(), name='campanha-criar'),
    path('campanha/<int:pk>', Dashboard.as_view(), name='dashboard'),

    path('painel/', ListarPainelADM.as_view(), name='painel-listar'),
    path('painel/campanhas', ListarPainelCampanhasADM.as_view(), name='painel-campanhas'),

]+ static (settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
