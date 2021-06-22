from rest_framework import serializers
from .models import Post, Comment


class CommentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = 'id text rating'.split()


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


# class CommentListSerializer(serializers.ModelSerializer):
#     post = PostItemSerializer()
#
#     class Meta:
#         model = Comment
#         fields = 'id created_date text rating'.split()
