from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from feature.models import Food, Category


class Profile(models.Model):
    user        = models.OneToOneField(
        User,
        primary_key = True,
        related_name= 'profile',
        verbose_name= 'user',
        on_delete   = models.CASCADE
    )

    nickname    = models.CharField(
        verbose_name= 'nickname',
        max_length  = 32
    )

    interest_in = models.ForeignKey(
        Category,
        related_name= 'interested',
        verbose_name= 'interest_in',
        blank       = True,
        null        = True,
        on_delete   = models.CASCADE
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
