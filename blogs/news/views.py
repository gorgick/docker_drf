from django.db.models import Prefetch, Count, F
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from news.models import Comment, Blog
from news.serializers import BlogSerializer


class BlogViewSet(ModelViewSet):
    queryset = Blog.objects.all().prefetch_related(Prefetch('comments', queryset=Comment.objects.all().annotate(
        owner_name=F('owner__username')))).prefetch_related('likes').annotate(
        author_name=F('owner__username')).annotate(likes_count=Count('likes'))
    serializer_class = BlogSerializer


