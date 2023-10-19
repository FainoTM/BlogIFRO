from django.contrib import admin
from .models import Postagem, Comentario


@admin.register(Postagem)
class PostagemAdmin(admin.ModelAdmin):
    list_display = ['autor','titulo', 'criado', 'status']
    list_editable = ['status']
    prepopulated_fields = {'slug':('titulo',)}
    ordering = ('-status', 'criado')


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'criado', 'status', 'ativo']
    list_editable = ['status', 'ativo',]
    ordering = ('criado',)