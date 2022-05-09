from django.db import models
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    created_at      = models.DateTimeField(
        verbose_name= 'created at',
        blank       = True, 
        null        = True, 
        auto_now_add= True
    )
    updated_at      = models.DateTimeField(
        verbose_name= 'updated at',
        blank       = True, 
        null        = True,
        auto_now    = True
    )

    class Meta:
        abstract    = True
