# Generated by Django 5.1.2 on 2024-10-20 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0006_alter_jogo_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='conta',
            field=models.FloatField(default=100),
        ),
    ]
