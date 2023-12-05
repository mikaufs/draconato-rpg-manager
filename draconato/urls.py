from django.contrib import admin
from django.urls import path, include
from manager.views import ListarInicio, ListarMCampanhas, CampanhaCreateView, Dashboard
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    
    path('', ListarInicio.as_view(),name='index'),
    path('minhascampanhas', ListarMCampanhas.as_view(), name='minhascampanhas'),
    path('campanha/criar', CampanhaCreateView.as_view(), name='campanha-criar'),
    path('campanha/<int:pk>', Dashboard.as_view(), name='dashboard'),

]+ static (settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
