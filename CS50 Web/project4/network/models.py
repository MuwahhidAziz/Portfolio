from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("self", symmetrical=False, related_name='followers', blank=True)

    @property
    def follower_count(self):
        return self.followers.all().count()

    @property
    def following_count(self):
        return self.following.all().count()

    def __str__(self):
        return f'{self.username}: following->{self.following_count} , followers->{self.follower_count}'

class Post(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.writer.username}: {self.content[:20]} , likes->{self.likes.all().count()}'

    @property
    def like_count(self):
        return self.likes.all().count()

    @property
    def lovers(self):
        return self.likes.all()
    
    