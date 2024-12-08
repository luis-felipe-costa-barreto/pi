from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_id = request.session['usuario_id']
    jogos_lista = Jogo.objects.all().order_by('nome')
    form = Porcurarjogo(request.GET or None)
    if form.is_valid():
        nome = form.cleaned_data.get('nome')
        if nome:
            jogos_lista = jogos_lista.filter(nome__icontains=nome)
    paginator = Paginator(jogos_lista, 5)
    page = request.GET.get('page', 1)
    try:
        jogos = paginator.page(page)
    except:
        jogos = paginator.page(1)
    contexto = {
        'form': form,
        'jogos': jogos,
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

def pagina_anuncio(request, id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_id = request.session['usuario_id']
    anuncio = get_object_or_404(Anuncio, id = id)
    contexto = {
        'anuncio': anuncio,
        'generos': Genero.objects.all(),
        'temas': Tema.objects.all(),
        'usuario': Usuario.objects.get(id=usuario_id)
    }
    return render (request, 'pagina_anuncio.html', contexto)

def filtro(request, id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_id = request.session['usuario_id']
    tema = get_object_or_404(Tema, id = id)
    contexto = {
        'tema': tema,
        'jogos': Jogo.objects.all(),
        'usuario': Usuario.objects.get(id=usuario_id),
        'temas': Tema.objects.all(),
        'generos': Genero.objects.all(),
    }
    return render(request, 'filtro.html', contexto)

def filtro2(request, id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_id = request.session['usuario_id']
    genero = get_object_or_404(Genero, id = id)
    contexto = {
        'genero': genero,
        'jogos': Jogo.objects.all(),
        'usuario': Usuario.objects.get(id=usuario_id),
        'temas': Tema.objects.all(),
        'generos': Genero.objects.all(),
    }
    return render(request, 'filtro2.html', contexto)


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

def compra_anuncio(request, anuncio_id):
    if 'usuario_id' not in request.session:
        return redirect('login') 
    usuario_id = request.session['usuario_id']
    usuario = Usuario.objects.get(id=usuario_id)
    anuncio = get_object_or_404(Anuncio, id=anuncio_id)


    if anuncio.jogo in usuario.jogos.all():
        messages.error(request, 'Você já possui este jogo.')
        return redirect('mercado')

    if usuario.conta >= anuncio.valor:
        usuario.conta -= anuncio.valor 
        usuario.jogos.add(anuncio.jogo) 
        usuario.save()
        messages.success(request, f'Você comprou {anuncio.jogo.nome} com sucesso!')
        anuncio.usuario.conta += anuncio.valor
        anuncio.usuario.jogos.remove(anuncio.jogo)
        anuncio.usuario.save()
        anuncio.delete()
    else:
        messages.error(request, 'Saldo insuficiente para comprar este jogo.')

    return redirect('mercado')

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

def perfil(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_id = request.session['usuario_id']
    usuario = Usuario.objects.get(id=usuario_id)
    contexto = {
        'usuario' : usuario,
        'jogos': Jogo.objects.all(),
        'lista': usuario.jogos.all()
    }
    return render (request, 'perfil.html', contexto)

def anunciar(request, id):
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_id = request.session['usuario_id']
    usuario = Usuario.objects.get(id=usuario_id)
    jogo = Jogo.objects.get(id=id)
    
    if request.method == 'POST':
        form = AnuncioForm(request.POST)
        if form.is_valid():
            resultado = form.save(commit=False)
            resultado.jogo = jogo
            resultado.usuario = usuario
            resultado.save()
            return redirect('biblioteca')
    else:
        form = AnuncioForm()

    contexto = {
        'usuario': usuario,
        'form': form,
        'jogo': jogo
    }
    return render(request, 'anuncio.html', contexto)

def mercado(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    usuario_id = request.session['usuario_id']
    usuario = Usuario.objects.get(id=usuario_id)
    anuncios = Anuncio.objects.all()
    contexto = {
        'usuario': usuario,
        'generos': Genero.objects.all(),
        'temas': Tema.objects.all(),
        'anuncios': anuncios
    }
    return render (request, 'mercado.html', contexto)

