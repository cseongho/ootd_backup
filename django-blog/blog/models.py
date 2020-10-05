import os
import datetime
from .utils import unique_slug_generator
from django.urls import reverse
from django.shortcuts import redirect
from django.db.models.signals import pre_save
from django.utils import timezone
from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User

# Create your models here.

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = datetime.datetime.now()
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    return f'products/{final_filename}'

class Category(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_by_category', kwargs={'slug': self.slug})


class Post(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True, null=True, blank=True)
    overview = models.TextField()
    content = HTMLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)
    thumbnail = models.ImageField(upload_to=upload_image_path)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def get_comments(self):
        return self.comments.all().order_by('-created_on')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.user.username

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)

def pre_save_category_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_category_receiver, sender=Category)