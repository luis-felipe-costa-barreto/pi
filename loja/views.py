from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password
# Create your views here.
def index(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_id = request.session['usuario_id']
    
    contexto = {
        'jogos': Jogo.objects.all(),
        'generos': Genero.objects.all(),
        'temas': Tema.objects.all(),
        'usuario': Usuario.objects.get(id=usuario_id)
    }
    return render (request, 'index.html', contexto)

def pagina_jogo(request, id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_id = request.session['usuario_id']
    jogo = get_object_or_404(Jogo, id = id)
    contexto = {
        'jogo': jogo,
        'generos': Genero.objects.all(),
        'temas': Tema.objects.all(),
        'usuario': Usuario.objects.get(id=usuario_id)
    }
    return render (request, 'pagina_jogo.html', contexto)

def biblioteca(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_id = request.session['usuario_id']
    usuario = Usuario.objects.get(id=usuario_id)
    contexto = {
        'jogos': Jogo.objects.all(),
        'usuario': usuario,
        'lista': usuario.jogos.all()     
    }
    return render (request, 'biblioteca.html', contexto)

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST, request.FILES)
        if form.is_valid():
            nome_usuario = form.cleaned_data['nome_usuario']
            email = form.cleaned_data['email']
            if Usuario.objects.filter(nome_usuario=nome_usuario).exists():
                messages.error(request, 'Nome de usuário já está em uso.')
                return render(request, 'cadastro.html', {'form': form})
            if Usuario.objects.filter(email=email).exists():
                messages.error(request, 'Email já está em uso.')
                return render(request, 'cadastro.html', {'form': form})
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('login')
    else:
        form = CadastroForm()
    return render(request, 'cadastro.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            nome_usuario = form.cleaned_data['nome_usuario']
            senha = form.cleaned_data['senha']

            try:
                usuario = Usuario.objects.get(nome_usuario=nome_usuario)
                if check_password(senha, usuario.senha):
                    request.session['usuario_id'] = usuario.id
                    messages.success(request, 'Login realizado com sucesso!')
                    return redirect('index') 
                else:
                    messages.error(request, 'Senha incorreta.')
            except Usuario.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def compra_jogo(request, jogo_id):
    if 'usuario_id' not in request.session:
        return redirect('login') 
    usuario_id = request.session['usuario_id']
    usuario = Usuario.objects.get(id=usuario_id)
    jogo = get_object_or_404(Jogo, id=jogo_id)


    if jogo in usuario.jogos.all():
        messages.error(request, 'Você já possui este jogo.')
        return redirect('index')

    if usuario.conta >= jogo.valor:
        usuario.conta -= jogo.valor 
        usuario.jogos.add(jogo) 
        usuario.save()
        messages.success(request, f'Você comprou {jogo.nome} com sucesso!')
    else:
        messages.error(request, 'Saldo insuficiente para comprar este jogo.')

    return redirect('index')

def excluir_conta(request):
    if 'usuario_id' not in request.session:
        return redirect('login')

    usuario_id = request.session['usuario_id']
    usuario = Usuario.objects.get(id=usuario_id)

    if request.method == 'POST':
        usuario.delete()
        del request.session['usuario_id']
        messages.success(request, 'Sua conta foi excluída com sucesso.')
        return redirect('login')

    return render(request, 'confirmar_exclusao.html', {'usuario': usuario})
