
from django.db import models
from django.utils.text import slugify
from category.models import Category
from django.urls import reverse


news = 'News'
article = 'Article'

BLOG_CHOICES = [
    (news, 'News'),
    (article, 'Article')
]

class Posts(models.Model):
    blog_type = models.CharField(
        max_length=20,
        choices=BLOG_CHOICES,
        default='Article'
    )
    title = models.CharField(max_length=75, blank=False)
    body = models.TextField(blank=False, default='Empty field')
    preview = models.CharField(max_length=127, blank=True)  # Интеграция поля preview
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)
    # author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name="PostCategory")
    # post_rating = models.IntegerField(default=0)

#Product.objects.filter(postcategory__name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        if not self.preview and self.body:
            self.preview = f"{self.body[:124]}..."

        super().save(*args, **kwargs)

    def post_like(self):
        self.post_rating += 1
        self.save()

    def post_dislike(self):
        self.post_rating -= 1
        self.save()

    def get_absolute_url_detail(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.title.title()}: {self.preview}' #({self.price})'

    class Meta:
        ordering = ['-id']

