from django.contrib import admin
from django.urls import path, include
from manager.views import Listar, TesteLogin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),

    path('', Listar.as_view(),name='index'),
    path('login', TesteLogin.as_view(), name='login'),
]+ static (settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
