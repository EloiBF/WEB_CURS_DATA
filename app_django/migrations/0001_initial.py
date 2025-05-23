# Generated by Django 5.2 on 2025-04-22 18:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Curs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, verbose_name='Nom del curs')),
                ('descripcio', models.TextField(blank=True, null=True, verbose_name='Descripció')),
                ('color_fons', models.CharField(default='#FFFFFF', max_length=7, verbose_name='Color de fons')),
            ],
        ),
        migrations.CreateModel(
            name='Capitol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titol', models.CharField(max_length=100, verbose_name='Títol del capítol')),
                ('numero', models.PositiveIntegerField(verbose_name='Número del capítol')),
                ('dificultat', models.CharField(max_length=50, verbose_name='Dificultat')),
                ('preu', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='Preu')),
                ('data_creacio', models.DateTimeField(auto_now_add=True, verbose_name='Data de creació')),
                ('curs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='capitols', to='app_django.curs', verbose_name='Curs')),
            ],
            options={
                'verbose_name': 'Capítol',
                'verbose_name_plural': 'Capítols',
                'ordering': ['numero'],
                'unique_together': {('curs', 'numero')},
            },
        ),
        migrations.CreateModel(
            name='Exercici',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.PositiveIntegerField(default=0, verbose_name="Número d'exercici")),
                ('titol', models.CharField(blank=True, max_length=200, null=True, verbose_name="Títol de l'exercici")),
                ('tipus', models.CharField(choices=[('codi', 'Codi'), ('test', 'Test'), ('text', 'Text lliure')], max_length=20, verbose_name="Tipus d'exercici")),
                ('descripcio', models.TextField(blank=True, null=True, verbose_name='Descripció')),
                ('enunciat', models.TextField(verbose_name='Enunciat')),
                ('resposta_usuari', models.TextField(blank=True, null=True, verbose_name="Resposta de l'usuari")),
                ('solucio', models.TextField(verbose_name='Solució correcta')),
                ('imatge_1', models.ImageField(blank=True, null=True, upload_to='exercicis/imatges/', verbose_name='Imatge 1')),
                ('descripcio_imatge_1', models.CharField(blank=True, max_length=255, null=True, verbose_name='Descripció imatge 1')),
                ('imatge_2', models.ImageField(blank=True, null=True, upload_to='exercicis/imatges/', verbose_name='Imatge 2')),
                ('descripcio_imatge_2', models.CharField(blank=True, max_length=255, null=True, verbose_name='Descripció imatge 2')),
                ('respostes_test', models.JSONField(blank=True, null=True, verbose_name='Respostes del test')),
                ('temps_estimat_minuts', models.IntegerField(blank=True, null=True, verbose_name='Temps estimat (min)')),
                ('pista_1', models.TextField(blank=True, null=True, verbose_name='Pista 1')),
                ('pista_2', models.TextField(blank=True, null=True, verbose_name='Pista 2')),
                ('capitol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercicis', to='app_django.capitol', verbose_name='Capítol')),
                ('curs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercicis', to='app_django.curs', verbose_name='Curs')),
            ],
            options={
                'verbose_name': 'Exercici',
                'verbose_name_plural': 'Exercicis',
                'ordering': ['capitol__numero', 'numero'],
                'unique_together': {('capitol', 'numero')},
            },
        ),
    ]
