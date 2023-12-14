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

    nome = models.CharField(max_length=100, default='nada')
    imagem = models.ImageField(upload_to='images/personagem')
    level = models.IntegerField(blank=True, default='0')
    ca = models.IntegerField(blank=True, default='0')
    vida = models.IntegerField(blank=True, default='0')
    classe = models.CharField(blank=True, max_length=100, default='0')
    raca = models.CharField(blank=True,max_length=100, default='0')
    deslocamento = models.CharField(blank=True,max_length=100, default='0')

    pericias = models.TextField(blank=True, default='0')
    mh = models.TextField(blank=True, default='0')
    inventario = models.TextField(blank=True, default='0')

    forca = models.IntegerField(blank=True, default='0')
    destreza = models.IntegerField(blank=True, default='0')
    constituicao = models.IntegerField(blank=True, default='0')
    inteligencia = models.IntegerField(blank=True, default='0')
    sabedoria = models.IntegerField(blank=True, default='0')
    carisma = models.IntegerField(blank=True, default='0')

    def __str__(self):
        return self.nome
    
class Postagem(models.Model):
    campanha = models.ForeignKey(Campanha,on_delete=models.CASCADE)
    autor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    texto = models.TextField()
    data_postagem = models.DateField(auto_now_add=True)
    hora_criacao = models.TimeField(auto_now_add=True)


    def __str__(self):
        return self.texto

