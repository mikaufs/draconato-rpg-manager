from django.shortcuts import render
from .models import *
from .forms import *
from django.views.generic import ListView,CreateView,DeleteView,DetailView, UpdateView,TemplateView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages import views

class Listar(LoginRequiredMixin, ListView):
    template_name = "manager/index.html"
    model = Campanha
    context_object_name = 'campanhas'

class TesteLogin(TemplateView):
    template_name = "manager/login.html"

class TesteDashboard(TemplateView):
    template_name = "manager/dashboard/dashboard.html"

# Create your views here.
