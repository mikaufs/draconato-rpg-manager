from django import forms
from django.contrib.auth.models import User
from .models import Campanha

class CampanhaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CampanhaForm, self).__init__(*args, **kwargs)

        queryset = User.objects.exclude(is_superuser=True)
        
        if user and user.is_authenticated:
            queryset = queryset.exclude(pk=user.pk)

        self.fields['jogador'].queryset = queryset

    class Meta:
        model = Campanha
        fields = ['imagem', 'nome', 'sistema', 'mestre', 'descricao', 'jogador']