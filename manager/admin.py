from django.contrib import admin
from .models import Campanha, Anotacao, Sistema, Personagem, Postagem

@admin.register(Sistema)
class CampanhaAdmin (admin.ModelAdmin):
    list_display = ['nome',]

@admin.register(Campanha)
class CampanhaAdmin (admin.ModelAdmin):
    list_display = ['nome', 'sistema', 'data_inicio', 'descricao', 'mestre']

@admin.register(Anotacao)
class AnotacaoAdmin (admin.ModelAdmin):
    list_display = ['campanha', 'titulo', 'autor', 'texto']

@admin.register(Personagem)
class PersonagemAdmin (admin.ModelAdmin):
    list_display = ['campanha', 'usuario', 'nome', 'level', 'ca', 'vida', 'classe']

@admin.register(Postagem)
class PostagemAdmin (admin.ModelAdmin):
    list_display = ['campanha', 'autor', 'texto', 'data_postagem']