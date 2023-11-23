from django.contrib import admin
from .models import Campanha, Anotacao, Sistema, Personagem

@admin.register(Sistema)
class CampanhaAdmin (admin.ModelAdmin):
    list_display = ['nome',]

@admin.register(Campanha)
class CampanhaAdmin (admin.ModelAdmin):
    list_display = ['nome', 'sistema', 'data_inicio', 'mestre']

@admin.register(Anotacao)
class AnotacaoAdmin (admin.ModelAdmin):
    list_display = ['campanha', 'titulo', 'autor', 'texto']

@admin.register(Personagem)
class PersonagemAdmin (admin.ModelAdmin):
    list_display = ['campanha', 'usuario', 'nome', 'level', 'ca', 'vida_max','vida']