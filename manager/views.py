from django.shortcuts import render
from .models import Campanha, Anotacao, Personagem
from .forms import CampanhaForm
from django.views.generic import ListView,CreateView,DeleteView,DetailView, UpdateView,TemplateView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages import views
from django.db.models import Q

class ListarMCampanhas(ListView):
    template_name = "manager/minhas_campanhas.html"
    model = Campanha
    context_object_name = 'campanhas'

    def get_queryset(self):
        user = self.request.user
        queryset = Campanha.objects.filter(Q(mestre=user) | Q(jogador=user))
        return queryset

class ListarInicio(LoginRequiredMixin, ListView):
    template_name = "manager/index.html"
    model = Campanha
    context_object_name = 'campanhas'
    paginate_by = '4'

    def get_queryset(self):
        user = self.request.user
        queryset = Campanha.objects.filter(Q(mestre=user) | Q(jogador=user))
        return queryset
    
class CampanhaCreateView(CreateView):
    model = Campanha
    form_class = CampanhaForm
    template_name = "manager/forms/form_campanha.html"
    success_url = reverse_lazy("minhascampanhas")

    def form_valid(self, form):
        form.instance.mestre = self.request.user
        return super().form_valid(form)

class TesteDashboard(TemplateView):
    template_name = "manager/dashboard/dashboard.html"

    def get_perm(self):
        user = self.request.user
        queryset = Campanha.objects.filter(Q(mestre=user) | Q(jogador=user))
        
        if user != queryset:
            return reverse_lazy('index')

def pesquisa(request):
    pesquisa = request.GET.get('pesq')
    Categ_str = request.GET.get('categ')

    Categ = 0
    if Categ_str is not None:
        try:
            Categ = int(Categ_str)
        except ValueError:
            Categ = 0

    if Categ == 0:
        lista = Campanha.objects.order_by('-id').filter(
            nome__icontains=pesquisa
        )
    else:
        lista = Campanha.objects.order_by('-id').filter(
            nome__icontains=pesquisa,
            categoria=Categ
        )
    print(lista)

    return render(request, 'pesquisa_campanhas.html', {
        'campanhas': lista,
    })