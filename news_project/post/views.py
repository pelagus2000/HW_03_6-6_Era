from django.views.generic import ListView, DetailView

from .models import Posts
from pprint import pprint



class PostsList(ListView):
    model = Posts
    ordering = '-id'
    # queryset = Product.objects.filter(
    #     price__lt=300
    # ).order_by(
    #     'name'
    # )
    template_name = 'posts.html'
    context_object_name = 'posts'

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


