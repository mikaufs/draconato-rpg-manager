from django import forms
from .models import Campanha

class CampanhaForm(forms.ModelForm):
    class Meta:
        model = Campanha
        fields = ['imagem', 'nome', 'sistema', 'mestre', 'descricao', 'jogador']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CampanhaForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['mestre'].initial = user