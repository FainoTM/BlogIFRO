# Generated by Django 4.2.5 on 2023-10-10 02:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('postagens', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=150)),
                ('senha', models.CharField(max_length=60)),
                ('publicado', models.DateTimeField(default=django.utils.timezone.now)),
                ('criado', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('rascunho', 'Rascunho'), ('publicado', 'Publicado')], default='rascunho', max_length=9)),
            ],
        ),
    ]
