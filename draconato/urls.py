from django.contrib import admin
from django.urls import path, include
from manager.views import ListarInicio, ListarMCampanhas, TesteDashboard
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    
    path('', ListarInicio.as_view(),name='index'),
    path('minhascampanhas', ListarMCampanhas.as_view(), name='minhascampanhas'),
    path('dashboard/<int:pk>', TesteDashboard.as_view(), name='dashboard'),

]+ static (settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
