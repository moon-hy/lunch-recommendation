from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.functions import Coalesce

from core.models import TimeStampedModel


class Tag(models.Model):

    name        = models.CharField(
        verbose_name= 'tag name',
        max_length  = 255
    )

    detail      = models.TextField(
        verbose_name= 'tag detail'
    )

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return self.name

class Category(models.Model):

    name        = models.CharField(
        verbose_name= 'category',
        max_length  = 255
    )

class Food(models.Model):

    name        = models.CharField(
        verbose_name= 'food name',
        max_length  = 255
    )

    detail      = models.TextField(
        verbose_name= 'food detail'
    )

    category    = models.ForeignKey(
        Category,
        related_name= 'foods',
        verbose_name= 'category',
        on_delete   = models.CASCADE
    )

    kcal        = models.IntegerField(
        verbose_name= 'kcal',
        default     = 0
    )

    image       = models.ImageField(
        verbose_name= 'image',
        upload_to   = 'food/images/'
    )

    tags        = models.ManyToManyField(
        Tag,
        related_name= 'foods',
        verbose_name= 'tags'
    )

    class Meta:
        db_table = 'food'

    def __str__(self):
        return self.name

    @property
    def rating_avg(self):
        return Review.objects.filter(food=self).aggregate(
                avg=Coalesce(
                    models.Avg('rating'), 
                    0, 
                    output_field=models.DecimalField(
                        max_digits      =4,
                        decimal_places  =2
                    )),
            )['avg']

class Review(TimeStampedModel):
    
    user        = models.ForeignKey(
        User,
        related_name= 'reviews',
        verbose_name= 'user',
        on_delete   = models.CASCADE
    )

    food        = models.ForeignKey(
        Food,
        related_name= 'reviews',
        verbose_name= 'food',
        on_delete   = models.CASCADE
    )

    rating      = models.IntegerField(
        verbose_name= 'rating',
        default     = 0,
        validators  = [
            MinValueValidator(0),
            MaxValueValidator(5),
        ]
    )

    content     = models.CharField(
        verbose_name= 'content',
        max_length  = 255,
    )
    
    class Meta:
        db_table = 'review'

    def __str__(self):
        return f'{self.food.name} | {self.rating}'
