from django.db import models

# Create your models here.
class Empresa(models.Model):
    nome = models.CharField(max_length=100, null=False)
    logo = models.ImageField(upload_to='logos/')   
    def __str__(self):
        return self.nome

class Genero(models.Model):
    nome = models.CharField(max_length=50, null=False)
    def __str__(self):
        return self.nome


class Tema(models.Model):
    nome = models.CharField(max_length=50, null=False)
    def __str__(self):
        return self.nome

class Jogo(models.Model):
    nome = models.CharField(max_length=100, null=False)
    valor = models.FloatField(null=False)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='ijogos/')
    temas = models.ManyToManyField(Tema)
    generos = models.ManyToManyField(Genero)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    def __str__(self):
        return self.nome

class Usuario(models.Model):
    nome = models.CharField(max_length=100, null = False)
    email = models.EmailField(null=False)
    senha = models.CharField(max_length=50, null=False)
    nome_usuario = models.CharField(max_length=50, null=False)
    perfil = models.ImageField(upload_to='perfis/')
    jogos = models.ManyToManyField(Jogo)
    conta = models.FloatField(default=1000)
    def __str__(self):
        return self.nome
