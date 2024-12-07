from django import forms
from .models import *
from django.contrib.auth.hashers import make_password

class CadastroForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))

    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'nome_usuario', 'perfil', 'senha']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'nome_usuario': forms.TextInput(attrs={'placeholder': 'Nome de Usuário'}),
            'perfil': forms.ClearableFileInput(attrs={'id': 'perfil'}),
        }

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.senha = make_password(self.cleaned_data['senha'])
        if commit:
            usuario.save()
        return usuario

class LoginForm(forms.Form):
    nome_usuario = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Nome de Usuário'}))
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))

class Porcurarjogo(forms.Form):
    nome = forms.CharField(max_length=100, required=False)