from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class PostsPublicados(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status='publicado')


class Postagem(models.Model):
    objects = models.Manager()
    publicados = PostsPublicados()
    STATUS_CHOICES = (
        ('rascunho', 'Rascunho'),
        ('publicado', 'Publicado'),
    )
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    corpo = models.TextField()
    publicado = models.DateTimeField(default=timezone.now)
    criado = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='rascunho')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_autor')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-publicado']

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    STATUS_CHOICES = (
        ('rascunho', 'Rascunho'),
        ('publicado', 'Publicado'),
    )
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    senha = models.CharField(max_length=60)
    publicado = models.DateTimeField(default=timezone.now)
    criado = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='rascunho')
    corpo = models.TextField()
    ativo = models.BooleanField(default=False)
    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"

    def __str__(self):
        return f'Comentário de: {self.nome}'
