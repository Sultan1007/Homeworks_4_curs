from django.contrib.auth.models import User
from django.db import models


class HashTag(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=50, verbose_name='title')
    text = models.TextField(max_length=100, verbose_name='text')
    created_date = models.DateField(auto_created=True, verbose_name='date')
    hash_tag = models.ManyToManyField(HashTag, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(verbose_name='comment')
    rating = models.IntegerField(default=5, null=True)
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.text


class PostLike(models.Model):
    post = models.ForeignKey(Post, null=True,
                             on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True,
                             on_delete=models.SET_NULL)
