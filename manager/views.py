from django.shortcuts import render, get_object_or_404
from .models import Campanha, Anotacao, Personagem, Postagem
from django.contrib.auth.models import User
from .forms import CampanhaForm, PostagemForm
from django.views.generic import ListView,CreateView,DeleteView,DetailView, UpdateView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.messages import views
from django.db.models import Q
from django.http import HttpResponseForbidden

class ListarMCampanhas(ListView):
    template_name = "manager/minhas_campanhas.html"
    model = Campanha
    context_object_name = 'campanhas'
    paginate_by='5'

    def get_queryset(self):
        search = self.request.GET.get('search')
        if search:
            campanhas = Campanha.objects.filter(nome__icontains=search)
        else:
            user = self.request.user
            campanhas = Campanha.objects.filter(Q(mestre=user) | Q(jogador=user))

        return campanhas

class ListarInicio(LoginRequiredMixin, ListView):
    template_name = "manager/index.html"
    model = Campanha
    context_object_name = 'campanhas'
    paginate_by = '4'

    def get_queryset(self):
        user = self.request.user
        queryset = Campanha.objects.filter(Q(mestre=user) | Q(jogador=user))
        return queryset
    
class CampanhaCreate(CreateView):
    model = Campanha
    form_class = CampanhaForm
    template_name = "manager/forms/form_campanha.html"
    success_url = reverse_lazy("minhascampanhas")
    
    def get(self, request, *args, **kwargs):
        
        form = CampanhaForm(user=request.user if request.user.is_authenticated else None)
        return render(request, self.template_name, {'form': form})

class Dashboard(DetailView):
    template_name = "manager/dashboard/dashboard.html"
    model = Campanha

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['postagens'] = Postagem.objects.filter(campanha=self.object).order_by('-hora_criacao')
        return context

    def get(self, request, *args, **kwargs):
        user = self.request.user
        queryset = Campanha.objects.filter(Q(mestre=user) | Q(jogador=user))

        if not queryset.exists():
            return reverse_lazy('index')

        return super().get(request, *args, **kwargs)
    
class ListarPainelADM(ListView):
    template_name = "manager/admin/painel.html"
    model = User
    context_object_name = "users"
    paginate_by = "5"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['campanhas'] = Campanha.objects.all()
        return context

class ListarPainelCampanhasADM(ListView):
    template_name = "manager/admin/painel_campanha.html"
    model = Campanha
    context_object_name = "campanhas"
    paginate_by = "5"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['users'] = User.objects.all()
        return context
    
class PostagemCreateView(CreateView):
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
