# Generated by Django 5.1.2 on 2024-10-19 17:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0004_remove_jogo_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='jogo',
            name='empresa',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='loja.empresa'),
        ),
    ]
