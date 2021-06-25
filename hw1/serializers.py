from django.core.exceptions import ValidationError
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
