from django.shortcuts import render, get_object_or_404
from .models import Campanha, Anotacao, Personagem
from .forms import CampanhaForm
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
    
class CampanhaCreateView(CreateView):
    model = Campanha
    form_class = CampanhaForm
    template_name = "manager/forms/form_campanha.html"
    success_url = reverse_lazy("minhascampanhas")
    

    def get(self, request, *args, **kwargs):
        
        form = CampanhaForm(user=request.user if request.user.is_authenticated else None)
        return render(request, self.template_name, {'form': form})

class Dashboard(TemplateView):
    template_name = "manager/dashboard/dashboard.html"

    def get_perm(self):
        user = self.request.user
        queryset = Campanha.objects.filter(Q(mestre=user) | Q(jogador=user))
        
        if user != queryset:
            return reverse_lazy('index')
# Create your views here.
