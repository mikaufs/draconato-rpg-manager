from django.shortcuts import render
from .models import *
from .forms import *
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

    def get_queryset(self):
        user = self.request.user
        queryset = Campanha.objects.filter(Q(mestre=user) | Q(jogador=user))
        return queryset

class TesteDashboard(TemplateView):
    template_name = "manager/dashboard/dashboard.html"

    def get_perm(self):
        user = self.request.user
        queryset = Campanha.objects.filter(Q(mestre=user) | Q(jogador=user))
        
        if user != queryset:
            return reverse_lazy('index')
# Create your views here.
