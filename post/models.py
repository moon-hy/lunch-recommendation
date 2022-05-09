from django.db import models
from django.contrib.auth.models import User

from core.models import *


class Post(TimeStampedModel):

    user        = models.ForeignKey(
        User,
        related_name= 'posts',
        verbose_name= 'user',
        on_delete   = models.CASCADE,
    )

    title       = models.CharField(
        verbose_name= 'title',
        max_length  = 255,
    )

    content     = models.TextField(
        verbose_name= 'content',
    )

    view_count  = models.IntegerField(
        verbose_name= 'view count',
        default     = 0
    )

    class Meta:
        db_table = 'posts'

    def __str__(self):
        return f'{self.user} | {self.title}'

    @property
    def comments_count(self):
        return self.comments.count()

    
class Comment(TimeStampedModel):

    user        = models.ForeignKey(
        User,
        related_name= 'comments',
        verbose_name= 'user',
        on_delete   = models.CASCADE
    )

    post        = models.ForeignKey(
        Post,
        related_name= 'comments',
        verbose_name= 'post', 
        on_delete   = models.CASCADE
    )

    content     = models.CharField(
        verbose_name= 'content',
        max_length  = 255,
    )

    class Meta:
        db_table = 'comments'
    
    def __str__(self):
        return f'{self.post} | {self.user} | {self.content}'
