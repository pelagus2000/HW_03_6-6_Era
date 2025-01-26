from django.db import models

from django.db import models
from django.contrib.auth.models import User



class Author(models.Model):
    author_name = models.CharField(max_length=75, blank=False, default='John Doe')
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.author_name

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#
#     avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
#     bio = models.TextField()
#
#     def __str__(self):
#         return self.user.username

