from django import forms
from django.contrib.auth.models import User
from .models import Campanha, Postagem, Personagem, Anotacao
from django.contrib.auth import get_user
from django.db.models import Q

class CampanhaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        mestre = kwargs.pop('mestre', None)
        super(CampanhaForm, self).__init__(*args, **kwargs)

        queryset = User.objects.exclude(is_superuser=True)

        if user and user.is_authenticated:
            queryset = queryset.exclude(pk=user.pk)

        if mestre:
            queryset = queryset.exclude(pk=mestre.pk)

        self.fields['jogador'].queryset = queryset

    class Meta:
        model = Campanha
        fields = ['imagem', 'nome', 'sistema', 'mestre', 'descricao', 'jogador']

class PostagemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PostagemForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['campanha'].queryset = Campanha.objects.filter(Q(mestre=self.user) | Q(jogador=self.user)).distinct()

    class Meta:
        model = Postagem
        fields = '__all__'

class PersonagemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PersonagemForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['campanha'].queryset = Campanha.objects.filter(Q(mestre=self.user) | Q(jogador=self.user)).distinct()

    class Meta:
        model = Personagem
        fields = '__all__'

class AnotacaoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        
        self.user = kwargs.pop('user', None)
        super(AnotacaoForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['campanha'].queryset = Campanha.objects.filter(Q(mestre=self.user) | Q(jogador=self.user)).distinct()

        queryset = User.objects.exclude(is_superuser=True)

        user = self.user

        if user and user.is_authenticated:
            queryset = queryset.exclude(pk=user.pk)

        self.fields['visibilidade'].queryset = queryset

    class Meta:
        model = Anotacao
        fields = '__all__'