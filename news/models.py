from django.db import models

# Create your models here.
class News(models.Model):
    key = models.CharField(max_length=100, unique=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.key