from django.shortcuts import render, get_object_or_404
from .models import Campanha, Anotacao, Personagem, Postagem
from django.contrib.auth.models import User
from .forms import CampanhaForm, PostagemForm, PersonagemForm
from django.views.generic import ListView,CreateView,DeleteView,DetailView, UpdateView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.messages import views
from django.db.models import Q
from django.http import HttpResponseForbidden

# - - - - - - - - - - # Minhas Campanhas # - - - - - - - - - - #

class ListarMCampanhas(LoginRequiredMixin ,ListView):
    template_name = "manager/minhas_campanhas.html"
    model = Campanha
    context_object_name = 'campanhas'
    paginate_by='5'

    def get_queryset(self):
        search = self.request.GET.get('search')
        user = self.request.user

        if search:
            campanhas = Campanha.objects.filter(Q(nome__icontains=search) & (Q(mestre=user) | Q(jogador=user))).distinct()
        else:
            campanhas = Campanha.objects.filter(Q(mestre=user) | Q(jogador=user)).distinct()

        return campanhas

class CampanhaCreate(LoginRequiredMixin, CreateView):
    model = Campanha
    form_class = CampanhaForm
    template_name = "manager/forms/form_campanha.html"
    success_url = reverse_lazy("minhascampanhas")
    
    def get(self, request, *args, **kwargs):
        
        form = CampanhaForm(user=request.user if request.user.is_authenticated else None)
        return render(request, self.template_name, {'form': form})

class CampanhaUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Campanha
    form_class = CampanhaForm
    template_name = "manager/forms/form_campanha.html"
    success_url = reverse_lazy("minhascampanhas")

    def test_func(self):
        campanha = self.get_object()
        is_mestre = self.request.user == campanha.mestre
        return (
            is_mestre or
            self.request.user.is_superuser
        )

    def get_form_kwargs(self):
        kwargs = super(CampanhaUpdate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['mestre'] = self.object.mestre
        return kwargs

class CampanhaDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Campanha
    template_name = "manager/messages/campanha_delete.html"
    success_url = reverse_lazy("minhascampanhas")

    def test_func(self):
        campanha = self.get_object()
        is_mestre = self.request.user == campanha.mestre
        return (
            is_mestre or
            self.request.user.is_superuser
        )

class CampanhaDeletePainel(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Campanha
    template_name = "manager/messages/campanha_delete.html"
    success_url = reverse_lazy("painel-campanhas")

    def test_func(self):
        campanha = self.get_object()
        return self.request.user == campanha.mestre or self.request.user.is_superuser
    
    def test_func(self):
        campanha = self.get_object()
        is_mestre = self.request.user == campanha.mestre
        return (
            is_mestre or
            self.request.user.is_superuser
        )

# - - - - - - - - - - # Página Inicial # - - - - - - - - - - #

class ListarInicio(LoginRequiredMixin, ListView):
    template_name = "manager/index.html"
    model = Campanha
    context_object_name = 'campanhas'
    paginate_by = '4'

    def get_queryset(self):
        user = self.request.user
        queryset = Campanha.objects.filter(Q(mestre=user) | Q(jogador=user)).distinct()
        return queryset
    
# - - - - - - - - - - # DASHBOARD # - - - - - - - - - - #

class Dashboard(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = "manager/dashboard/dashboard.html"
    model = Campanha

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['postagens'] = Postagem.objects.filter(campanha=self.object).order_by('-data_postagem','-hora_criacao')
        return context

    def get(self, request, *args, **kwargs):
        user = self.request.user
        queryset = Campanha.objects.filter(Q(mestre=user) | Q(jogador=user))

        if not queryset.exists():
            return reverse_lazy('index')

        return super().get(request, *args, **kwargs)
    
    def test_func(self):
        campanha = self.get_object()
        is_mestre = self.request.user == campanha.mestre
        is_jogador = self.request.user in campanha.jogador.all()
        return (
            is_mestre or
            is_jogador or
            self.request.user.is_superuser
        )

    
class DashboardFichas(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = 'manager/dashboard/fichas.html'
    model = Campanha

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        campanha = self.get_object()

        is_mestre = campanha.mestre == user

        if is_mestre:
            context['personagens'] = Personagem.objects.filter(campanha=campanha)
        else:
            context['personagens'] = Personagem.objects.filter(campanha=campanha, usuario=user)

        return context
    
    def test_func(self):
        campanha = self.get_object()
        is_mestre = self.request.user == campanha.mestre
        is_jogador = self.request.user in campanha.jogador.all()
        return (
            is_mestre or
            is_jogador or
            self.request.user.is_superuser
        )

class FichaCreateView(LoginRequiredMixin, CreateView):
    model = Personagem
    template_name = "manager/forms/form_ficha.html"
    form_class = PersonagemForm
    success_url = reverse_lazy("dashboard-fichas")

    def get_form_kwargs(self):
        kwargs = super(FichaCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        initial = super(FichaCreateView, self).get_initial()
        initial['campanha'] = self.kwargs.get('pk')
        return initial
    
    def get_success_url(self):
        return reverse_lazy('dashboard-fichas', args=[self.object.campanha.pk])
    
    def test_func(self):
        personagem = self.get_object()
        return self.request.user == personagem.usuario or self.request.user == personagem.campanha.mestre or self.request.user.is_superuser

class FichaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Personagem
    template_name = "manager/forms/form_ficha.html"
    form_class = PersonagemForm
    success_url = reverse_lazy("dashboard-fichas")

    def get_initial(self):
        initial = super(FichaUpdateView, self).get_initial()
        initial['campanha'] = self.kwargs.get('pk')
        return initial
    
    def get_success_url(self):
        return reverse_lazy('dashboard-fichas', args=[self.object.campanha.pk])
    
    def test_func(self):
        personagem = self.get_object()
        return self.request.user == personagem.usuario or self.request.user == personagem.campanha.mestre or self.request.user.is_superuser
    
class FichaDeleteView(LoginRequiredMixin, DeleteView):
    model = Personagem
    template_name = 'manager/messages/ficha_delete.html'
    success_url = reverse_lazy('dashboard-fichas')
    
    def get_success_url(self):
        return reverse_lazy('dashboard-fichas', args=[self.object.campanha.pk])

# - - - - - - - - - - # CRUD - Painel (ADMIN) # - - - - - - - - - - #

class ListarPainelADM(UserPassesTestMixin, ListView):
    template_name = "manager/admin/painel.html"
    model = User
    context_object_name = "users"
    paginate_by = "5"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['campanhas'] = Campanha.objects.all()
        return context
    
    def test_func(self):
        return self.request.user.is_superuser

class ListarPainelCampanhasADM(UserPassesTestMixin, ListView):
    template_name = "manager/admin/painel_campanha.html"
    model = Campanha
    context_object_name = "campanhas"
    paginate_by = "5"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['users'] = User.objects.all()
        return context
    
    def test_func(self):
        return self.request.user.is_superuser

# - - - - - - - - - - # CRUD - Postagem (DASHBOARD) # - - - - - - - - - - #

class PostagemCreateView(LoginRequiredMixin, CreateView):
    model = Postagem
    template_name = "manager/forms/form_postagem.html"
    form_class = PostagemForm
    success_url = reverse_lazy("dashboard")

    def get_form_kwargs(self):
        kwargs = super(PostagemCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        initial = super(PostagemCreateView, self).get_initial()
        initial['campanha'] = self.kwargs.get('pk')
        return initial
    
    def get_success_url(self):
        return reverse_lazy('dashboard', args=[self.object.campanha.pk])
    
class PostagemUpdateView(LoginRequiredMixin, UpdateView):
    model = Postagem
    template_name = "manager/forms/form_postagem.html"
    form_class = PostagemForm
    success_url = reverse_lazy("dashboard")

    def get_success_url(self):
        return reverse_lazy('dashboard', args=[self.object.campanha.pk])
    
class PostagemDeleteView(LoginRequiredMixin,DeleteView):
    model = Postagem
    template_name = "manager/messages/postagem_delete.html"
    success_url = reverse_lazy("dashboard")
    
    def get_success_url(self):
        return reverse_lazy('dashboard', args=[self.object.campanha.pk])
