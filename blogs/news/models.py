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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__mark = self.mark

    def save(self, *args, **kwargs):
        if self.mark != self.__mark:
            annotated_likes.delay(Like.objects.filter(blog__id=self.blog_id).first())
        super().save(*args, **kwargs)
