from rest_framework.decorators import api_view
# Create your views here.
from hw1.models import Post, Comment
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from hw1.serializers import PostListSerializer, CommentItemSerializer


@api_view(['GET'])
def post_list_views(request):
    posts = Post.objects.all()
    data = PostListSerializer(posts, many=True).data
    return Response(data=data)


@api_view(['GET'])
def post_item_view(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        raise NotFound('Not found')
    data = PostListSerializer(post, many=False).data
    return Response(data=data)


@api_view(['GET'])
def comment_list(request):
    comment = Comment.objects.all()
    data = CommentItemSerializer(comment, many=True).data
    return Response(data=data)


@api_view(['GET'])
def comment_item(request, id):
    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        raise NotFound('Not found')
    data = CommentItemSerializer(comment, many=False).data
    return Response(data=data)
