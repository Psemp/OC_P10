from django.db import models
from django.contrib.auth.models import User
from research.models import Product


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(default='default.jpg', upload_to='profile_imgs')
    favorite = models.ManyToManyField(Product, related_name='favorites', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
