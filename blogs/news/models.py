from django.db import models
from django.contrib.auth import get_user_model
from news.tasks import annotated_likes

User = get_user_model()


class Blog(models.Model):
    title = models.CharField(max_length=100)
    article = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    likes_count = models.PositiveIntegerField(default=0)

    def save(self, *args, save_model=True, **kwargs):
        if save_model:
            annotated_likes.delay(self.id)
        super().save(*args, **kwargs)


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()


class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    mark = models.BooleanField(default=False)
