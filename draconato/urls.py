from django.contrib import admin
from django.urls import path, include
from manager.views import ListarInicio, ListarMCampanhas, CampanhaCreate, CampanhaUpdate, CampanhaDelete, CampanhaDeletePainel,Dashboard, DashboardFichas, DashboardAnotacoes, FichaCreateView, FichaUpdateView, FichaDeleteView, ListarPainelADM, ListarPainelCampanhasADM, PostagemCreateView, PostagemDeleteView, PostagemUpdateView, AnotacaoCreateView, AnotacaoUpdateView, AnotacaoDeleteView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    
    path('', ListarInicio.as_view(),name='index'),
    path('minhascampanhas', ListarMCampanhas.as_view(), name='minhascampanhas'),

    path('campanha/criar', CampanhaCreate.as_view(), name='campanha-criar'),
    path('campanha/<int:pk>/editar', CampanhaUpdate.as_view(), name='campanha-editar'),
    path('campanha/<int:pk>/deletar', CampanhaDelete.as_view(), name='campanha-deletar'),
    path('campanha/<int:pk>', Dashboard.as_view(), name='dashboard'),

    path('campanha/<int:pk>/fichas', DashboardFichas.as_view(), name='dashboard-fichas'),
    path('campanha/<int:pk>/ficha/criar', FichaCreateView.as_view(), name='ficha-create'),
    path('campanha/ficha/<int:pk>/editar', FichaUpdateView.as_view(), name='ficha-update'),
    path('campanha/ficha/<int:pk>/deletar', FichaDeleteView.as_view(), name='ficha-delete'),

    path('campanha/<int:pk>/postagem/criar', PostagemCreateView.as_view(), name='postagem-criar'),
    path('campanha/postagem/excluir/<int:pk>', PostagemDeleteView.as_view(), name='postagem-delete'),
    path('campanha/postagem/editar/<int:pk>', PostagemUpdateView.as_view(), name='postagem-update'),

    path('campanha/<int:pk>/anotacoes', DashboardAnotacoes.as_view(), name='dashboard-anotacoes'),
    path('campanha/<int:pk>/anotacao/criar', AnotacaoCreateView.as_view(), name='anotacao-create'),
    path('campanha/anotacao/editar/<int:pk>', AnotacaoUpdateView.as_view(), name='anotacao-update'),
    path('campanha/anotacao/deletar/<int:pk>', AnotacaoDeleteView.as_view(), name='anotacao-delete'),

    path('painel/usuarios', ListarPainelADM.as_view(), name='painel-listar'),
    path('painel/campanhas', ListarPainelCampanhasADM.as_view(), name='painel-campanhas'),
    path('painel/campanha/<int:pk>/deletar', CampanhaDeletePainel.as_view(), name='painel-campanha-deletar'),

]+ static (settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
