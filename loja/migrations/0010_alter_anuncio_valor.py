# Generated by Django 5.1.4 on 2024-12-08 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0009_anuncio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anuncio',
            name='valor',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
