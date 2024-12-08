"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from loja.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('biblioteca/', biblioteca, name='biblioteca'),
    path('pagina_jogo/<int:id>', pagina_jogo, name='pagina_jogo'),
    path('pagina_anuncio/<int:id>', pagina_anuncio, name='pagina_anuncio'),
    path('filtro/<int:id>', filtro, name='filtro'),
    path('filtro2/<int:id>', filtro2, name='filtro2'),
    path('cadastro/', cadastro, name='cadastro'),
    path('login/', login, name='login'),
    path('compra_jogo/<int:jogo_id>/', compra_jogo, name='compra_jogo'),
    path('compra_anuncio/<int:anuncio_id>/', compra_anuncio, name='compra_anuncio'),
    path('excluir_conta/', excluir_conta, name='excluir_conta'),
    path('perfil/', perfil, name='perfil'),
    path('mercado/', mercado, name='mercado'),
    path('anunciar/<int:id>', anunciar, name='anunciar'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

