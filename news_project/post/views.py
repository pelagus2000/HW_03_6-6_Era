from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostsFilter
from .models import Posts
from pprint import pprint
from .forms import NewsForm, ArticleForm
from django.urls import reverse_lazy

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

class PostsDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Posts
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['next post'] = None
        comment = "Нехороший человек — редиска!"
        context['comment'] = comment
        pprint(context)
        return context

class NewsCreate(CreateView):
    form_class = NewsForm
    model = Posts
    template_name = 'news_edit.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form):
        # Устанавливаем тип блога как 'News' перед сохранением
        form.instance.blog_type = 'News'
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = ArticleForm
    model = Posts
    template_name = 'article_edit.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form):
        # Устанавливаем тип блога как 'Article' перед сохранением
        form.instance.blog_type = 'Article'
        return super().form_valid(form)

class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = Posts
    template_name = 'news_edit.html'

class NewsDelete(DeleteView):
    model = Posts
    template_name = 'news_delete.html'
    success_url = reverse_lazy('posts_list')

class ArticleUpdate(UpdateView):
    form_class = ArticleForm
    model = Posts
    template_name = 'news_edit.html'

class ArticleDelete(DeleteView):
    model = Posts
    template_name = 'article_delete.html'
    success_url = reverse_lazy('posts_list')