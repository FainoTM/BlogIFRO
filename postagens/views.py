from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView

from postagens.forms import EmailForm, ComentarioModelForm, CadUsuarioForm
from postagens.models import Postagem, Comentario


class HomeView(TemplateView):
    template_name = 'index.html'


"""
class PostsListView(TemplateView):
    template_name = 'postagens/listar.html'

    def get_context_data(self, **kwargs):
        cont = super().get_context_data(**kwargs)
        cont['posts'] = Postagem.publicados.all()
        return cont
"""


class PostsListView(ListView):
    template_name = 'postagens/listar.html'
    queryset = Postagem.publicados.all()
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(PostsListView, self).get_context_data(**kwargs)
        for post in context['posts']:
            post.coments_count = self.get_comment_count(post.id)
        return context

    def get_comment_count(self, post_id):
        try:
            return len(Comentario.objects.filter(postagem_id=post_id))
        except Comentario.DoesNotExist:
            return 0


class DetalhePostView(DetailView):
    template_name = 'postagens/detalhe.html'
    model = Postagem

    def _get_coments(self, id_post):
        try:
            return Comentario.objects.filter(postagem_id=id_post, ativo = True)
        except Comentario.DoesNotExist:
            raise Exception

    def get_context_data(self, **kwargs):
        context = super(DetalhePostView, self).get_context_data(**kwargs)
        context['coments'] = self._get_coments(self.object.id)
        return context


class EnviarPostFormView(FormView):
    template_name = "postagens/enviar.html"
    form_class = EmailForm
    success_url = reverse_lazy('listarposts')

    def _get_postagem(self, idpost):
        try:
            return Postagem.publicados.get(id=idpost)
        except Postagem.DoesNotExist:
            messages.error(self.request, 'A postagem não existe!')
            reverse_lazy('listarposts')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        print(self.kwargs['pk'])
        ctx['post'] = self._get_postagem(self.kwargs['pk'])
        return ctx

    def form_valid(self, form):
        post = self.get_context_data()['post']
        # post = self._get_postagem(self.kwargs['pk'])
        messages.success(self.request, f'Postagem {post.titulo} '
                                       f'enviado com sucesso!!!')
        form.send_mail(post)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Não foi possível enviar a Postagem')
        return super().form_invalid(form)


class ComentarioCreateView(CreateView):
    template_name = "postagens/comentario.html"
    form_class = ComentarioModelForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['post'] = Postagem.objects.get(id=self.kwargs['pk'])
        return ctx

    def form_valid(self, form):
        post = Postagem.objects.get(id=self.kwargs['pk'])
        form.salvarComentario(post)
        return redirect('detalhepost', post.id, post.slug)


class CadUsuarioView( CreateView):
    template_name = 'usuarios/cadastro.html'
    form_class = CadUsuarioForm
    success_url = reverse_lazy('loginuser')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, message='Usuario Cadastrado!!!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Não foi possível cadastrar')
        redirect('cadusuario')


class LoginUserView(FormView):
    template_name = 'usuarios/login.html'
    model = User
    form_class = AuthenticationForm
    success_url = reverse_lazy('listarposts')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        senha = form.cleaned_data['password']
        usuario = authenticate(self.request, username = username, password = senha)
        if usuario is not None:
            login(self.request, usuario)
            return redirect('listarposts')
        messages.error(self.request, 'Usuário não cadastrado')
        return redirect('loginuser')

    def form_invalid(self, form):
        messages.error(self.request, 'Não foi possível logar')
        return redirect('loginuser')


class LogoutUserView(LoginRequiredMixin, LogoutView):

    def get(self, request):
        logout(request)
        return redirect('listarposts')

