from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=75, unique=True)

    def __str__(self):
        return self.name