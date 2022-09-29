from unittest.util import _MAX_LENGTH
from django.db import models
from django.forms import CharField, DateField, ImageField, SlugField
from datetime import date
# Create your models here.

class AuthorModel(models.Model):
    first_name = models.CharField(max_length = 50, default = '')
    last_name = models.CharField(max_length = 50, default = '')

    def __str__(self):
        return (self.first_name + ' ' + self.last_name)

class PostModel(models.Model):
    author = models.ForeignKey(
        AuthorModel, on_delete=models.SET_NULL, null = True,related_name= "posts")
    title=  models.CharField(max_length = 50,default = '')
    excerpt = models.CharField(max_length = 200,default = '')
    image = models.ImageField(upload_to = "posts", null = True)
    date=  models.DateField(auto_now = True) 
    slug = models.SlugField(unique = True, db_index = True)
    content = models.TextField(default = '')

    def __str__(self):
        return (self.title)

class CommentModel(models.Model):
    author = models.CharField(max_length = 50)
    content = models.CharField(max_length = 300)
    author_mail = models.EmailField()
    post= models.ForeignKey(
        PostModel, on_delete=models.CASCADE, null = True,related_name= "comments")

    