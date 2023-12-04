from django.db import models
from django.contrib.auth import get_user_model
    
class Sistema(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Campanha(models.Model):
    imagem = models.ImageField(upload_to='campanha/images/')
    nome = models.CharField(max_length=100)
    sistema = models.ForeignKey(Sistema, on_delete=models.CASCADE)
    data_inicio = models.DateField(auto_now_add=True)
    descricao = models.TextField(blank=True)
    mestre = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    jogador = models.ManyToManyField(get_user_model(), related_name='campanhas_participantes', blank=True)

    def __str__(self):
        return self.nome

class Anotacao(models.Model):
    campanha = models.ForeignKey(Campanha,on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    autor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    texto = models.TextField()
    visibilidade = models.ManyToManyField(get_user_model(), blank=True, related_name='anotacoes_visiveis')

    def __str__(self):
        return self.titulo

class Personagem(models.Model):
    campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE)
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    nome = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='images/personagem')
    level = models.IntegerField(default=1)
    ca = models.IntegerField(default=10)
    vida_max = models.IntegerField(default=10)
    vida = models.IntegerField(default=8)

    def __str__(self):
        return self.nome
