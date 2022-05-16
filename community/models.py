from django.db import models
from django.contrib.auth.models import User

from core.models import *


class Category(models.Model):

    name        = models.CharField(
        verbose_name= 'category name',
        max_length  = 127,
    )

    class Meta:
        db_table = 'community_category'
        ordering = ['name']

    def __str__(self):
        return self.name

class CustomModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'user', 'user__profile', 'category',
        ).prefetch_related(
            'comments', 'comments__user',
        ).annotate(
            comments_count=models.Count('comments')
        )

class Post(TimeStampedModel):

    user        = models.ForeignKey(
        User,
        related_name= 'posts',
        verbose_name= 'user',
        on_delete   = models.CASCADE,
    )

    category    = models.ForeignKey(
        Category,
        verbose_name= 'category',
        on_delete   = models.CASCADE
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

    objects     = CustomModelManager()

    class Meta:
        db_table = 'community_post'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} | {self.user}'

    # @property
    # def comments_count(self):
    #     return self.comments.count()

    
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
        db_table = 'community_comment'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.post} | {self.user} | {self.content}'
