from django.shortcuts import render, redirect
from .models import *
# Create your views here.
def index(request):
    contexto = {
        'jogos': Jogo.objects.all()
    }
    return render (request, 'index.html', contexto)