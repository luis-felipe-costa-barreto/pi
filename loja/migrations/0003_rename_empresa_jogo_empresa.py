# Generated by Django 5.1.2 on 2024-10-19 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0002_jogo_empresa'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jogo',
            old_name='Empresa',
            new_name='empresa',
        ),
    ]
