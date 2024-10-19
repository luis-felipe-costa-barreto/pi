from django.shortcuts import render, redirect
from .models import *
# Create your views here.
def index(request):
    contexto = {
        'jogos': Jogo.objects.all(),
        'generos': Genero.objects.all(),
        'temas': Tema.objects.all()
    }
    return render (request, 'index.html', contexto)

def biblioteca(request):
    contexto = {
        'jogos': Jogo.objects.all(),
        'usuarios': Usuario.objects.all()
    }
    return render (request, 'biblioteca.html', contexto)