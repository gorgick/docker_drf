from rest_framework import serializers

from news.models import Blog, Like, Comment


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('mark', 'blog', 'owner')


class CommentSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = ('text', 'owner_name')


class BlogSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(read_only=True, many=True)
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Blog
        fields = ('id', 'title', 'owner', 'article', 'comments', 'author_name', 'likes', 'likes_count')