from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.functional import empty
from rest_framework import serializers
from .models import Post, Comment


class CommentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = 'id text rating'.split()


class CommentsValidateSerializer(serializers.Serializer):
    comment = serializers.CharField(min_length=2, max_length=100)

    def validated_comment(self, object):
        if Comment.objects.filter(name=object).count() > 0:
            raise ValidationError("Такой коммент уже есть!")
        else:
            return object


class PostListSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = 'id title text comment count'.split()

    def get_comment(self, instance):
        comments = Comment.objects.filter(post_id=instance)
        return CommentItemSerializer(comments, many=True).data

    def get_count(self, obj):
        com = Comment.objects.filter(post=obj).count()
        return com


class PostItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = 'id title text'.split()


class PostsValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=100)
    text = serializers.CharField(min_length=5)

    def validate(self, object):
        object = object["title"]
        if Post.objects.filter(title=object).count() > 0:
            raise ValidationError("Такой пост уже есть!")
        else:
            return object


# class CommentListSerializer(serializers.ModelSerializer):
#     post = PostItemSerializer()
#
#     class Meta:
#         model = Comment
#         fields = 'id created_date text rating'.split()


class UserLoginValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=1000)
    password = serializers.CharField(max_length=1000)


class UserRegisterValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=1000)
    password = serializers.CharField(max_length=1000)
    password1 = serializers.CharField(max_length=1000)

    def __init__(self, instance=None, data=empty, ):
        super().__init__(instance, data, )
        self.cleaned_data = None

    def validate_username(self, username):
        if User.objects.filter(username=username).count() > 0:
            raise ValidationError('Пользователь уже существует')

    def clean_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise ValidationError('Пароли не совпадают')
        return self.cleaned_data['password']
