# Generated by Django 4.2.5 on 2023-10-11 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postagens', '0003_alter_comentario_options_comentario_postagem'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='corpo',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]