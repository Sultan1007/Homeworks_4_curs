from rest_framework import status
from rest_framework.decorators import api_view
# Create your views here.
from hw1.models import Post, Comment
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from hw1.serializers import PostListSerializer, CommentItemSerializer, CommentsValidateSerializer, \
    PostsValidateSerializer


@api_view(['GET', 'POST'])
def post_list_views(request):
    if request.method == "POST":

        serializer = PostsValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    'message': 'ERROR',
                    'errors': serializer.errors
                }
            )
        post = Post.objects.create(title=request.data["title"], text=request.data["text"])
        return Response(data={'message': 'created'})
    else:
        posts = Post.objects.all()
        data = PostListSerializer(posts, many=True).data
        return Response(data={'list': data})


@api_view(['GET'])
def post_item_view(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        raise NotFound('Not found')
    data = PostListSerializer(post, many=False).data
    return Response(data=data)


@api_view(['GET'])
def comment_list_view(request):
    comment = Comment.objects.all()
    data = CommentItemSerializer(comment, many=True).data
    return Response(data=data)


@api_view(['GET'])
def comment_item_view(request, id):
    if request.method == "POST":

        serializer = CommentsValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    'message': 'ERROR',
                    'errors': serializer.errors
                }
            )
        post = Post.objects.get(id=id)
        text = request.data.get('comment', '')
        Comment.objects.create(text=text, post_id=post.id)
        return Response(data={'message': 'created'})
    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        raise NotFound('Not found')
    data = CommentItemSerializer(comment, many=False).data
    return Response(data=data)
