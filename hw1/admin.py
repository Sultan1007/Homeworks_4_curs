from django.contrib import admin

# Register your models here.
from .models import Post, Comment, HashTag, PostLike

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(HashTag)
admin.site.register(PostLike)
