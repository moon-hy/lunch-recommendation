from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import TimeStampedModel
from food.models import Food


class Record(TimeStampedModel):

    user        = models.ForeignKey(
        User,
        related_name= 'records',
        verbose_name= 'user',
        on_delete   = models.CASCADE
    )

    food        = models.ForeignKey(
        Food,
        related_name= 'records',
        verbose_name= 'food',
        on_delete   = models.CASCADE
    )

    class Meta:
        db_table = 'record'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.food} | {self.created_at}'

class Profile(models.Model):
    user        = models.OneToOneField(
        User,
        related_name= 'profile',
        verbose_name= 'user',
        on_delete   = models.CASCADE
    )

    nickname    = models.CharField(
        verbose_name= 'nickname',
        max_length  = 32
    )

    likes       = models.ManyToManyField(
        Food,
        related_name= 'like_users',
        verbose_name= 'like_foods',
        blank       = True
    )

    dislikes    = models.ManyToManyField(
        Food,
        related_name= 'dislike_users',
        verbose_name= 'dislike_foods',
        blank       = True
    )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
