# Generated by Django 5.1.4 on 2024-12-08 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0010_alter_anuncio_valor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anuncio',
            name='valor',
            field=models.FloatField(),
        ),
    ]
