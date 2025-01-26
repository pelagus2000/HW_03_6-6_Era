from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostsFilter
from .models import Posts
from pprint import pprint
from .forms import NewsForm, ArticleForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# from django.shortcuts import redirect
#
# def index(request):
#     return redirect('post:post')

class PostsList(ListView):
    model = Posts
    ordering = '-id'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        # Оригинальный запрос
        queryset = super().get_queryset()

        # Инициализация фильтра
        self.filterset = PostsFilter(self.request.GET, queryset)

        # Если фильтр неподключён или запрос пустой, возвращаем полный набор записей
        if not any(self.request.GET.values()) or not self.filterset.is_valid():
            return queryset

        # Если есть применённые фильтры, возвращаем отфильтрованные записи
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

from django.contrib.auth.mixins import PermissionRequiredMixin

class PostsDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Posts
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'
    # Разрешаем доступ только пользователям в группе "author"
    permission_required = 'post.view_posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['next post'] = None
        comment = "Нехороший человек — редиска!"
        context['comment'] = comment
        pprint(context)
        return context


@method_decorator(login_required, name='dispatch')
class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = NewsForm
    model = Posts
    template_name = 'news_edit.html'
    success_url = reverse_lazy('posts_list')

    permission_required = 'post.add_posts'

    def form_valid(self, form):
        # Устанавливаем тип блога как 'News' перед сохранением
        form.instance.blog_type = 'News'
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ArticleCreate(PermissionRequiredMixin, CreateView):
    form_class = ArticleForm
    model = Posts
    template_name = 'article_edit.html'
    success_url = reverse_lazy('posts_list')

    permission_required = 'post.add_posts'

    def form_valid(self, form):
        # Устанавливаем тип блога как 'Article' перед сохранением
        form.instance.blog_type = 'Article'
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    form_class = NewsForm
    model = Posts
    template_name = 'news_edit.html'
    permission_required = 'post.change_posts'
    success_url = reverse_lazy('posts_list')


class NewsDelete(PermissionRequiredMixin, DeleteView):
    model = Posts
    template_name = 'news_delete.html'
    success_url = reverse_lazy('posts_list')
    permission_required = 'post.delete_posts'


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    form_class = ArticleForm
    model = Posts
    template_name = 'news_edit.html'
    permission_required = 'post.change_posts'
    success_url = reverse_lazy('posts_list')


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    model = Posts
    template_name = 'article_delete.html'
    success_url = reverse_lazy('posts_list')
    permission_required = 'post.delete_posts'