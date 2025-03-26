from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

# Create your models here.

class post(models.Model):

    title = models.CharField(max_length=100)
    content = models.TextField()
    img_url = models.URLField()
    create_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class aboutus(models.Model):
    content = models.TextField()
    
class img(models.Model):
    imgs = models.URLField()

class offer(models.Model):
    offers = models.URLField()

class Order(models.Model):
    recipe_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15)
    location = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.recipe_name
    
class CustomUser(AbstractUser):
    photo = models.ImageField( upload_to='profile_image', height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return self.username