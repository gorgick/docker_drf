import time

from celery import shared_task
from django.db.models import Count


@shared_task
def annotated_likes(blog_id):
    from news.models import Blog
    time.sleep(5)
    blog = Blog.objects.filter(id=blog_id).prefetch_related('likes').annotate(likes_counted=Count('likes')).first()
    blog.likes_count = blog.likes_counted
    blog.save(save_model=False)
