from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.functions import Coalesce

from core.models import TimeStampedModel


class Category(models.Model):

    name        = models.CharField(
        verbose_name= 'category',
        max_length  = 255
    )

    class Meta:
        db_table = 'feature_category'
        ordering = ['name']

    def __str__(self):
        return self.name
    @property
    def count_foods(self):
        return self.foods.count()

class Food(models.Model):

    category    = models.ForeignKey(
        Category,
        related_name= 'foods',
        verbose_name= 'category',
        on_delete   = models.CASCADE
    )

    name        = models.CharField(
        verbose_name= 'food name',
        max_length  = 255
    )

    detail      = models.TextField(
        verbose_name= 'food detail'
    )

    kcal        = models.IntegerField(
        verbose_name= 'kcal',
        default     = 0
    )

    image       = models.ImageField(
        verbose_name= 'image',
        upload_to   = 'food/images/',
        blank       = True,
        null        = True,
    )

    class Meta:
        db_table = 'feature_food'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def reviews(self):
        return Review.objects.filter(history__food=self)

    @property
    def rating_avg(self):
        return self.reviews.aggregate(
                avg=Coalesce(
                    models.Avg('rating'), 
                    0, 
                    output_field=models.DecimalField(
                        max_digits      =4,
                        decimal_places  =2
                    )),
            )['avg']

    @property
    def reviews_count(self):
        return self.reviews.count()

class History(TimeStampedModel):

    food        = models.ForeignKey(
        Food,
        related_name= 'histories',
        verbose_name= 'food',
        on_delete   = models.CASCADE
    )

    user        = models.ForeignKey(
        User,
        related_name= 'histories',
        verbose_name= 'user',
        on_delete   = models.CASCADE
    )

    class Meta:
        db_table = 'feature_history'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.profile.nickname} | {self.food} | {self.created_at}'

    @property
    def is_reviewed(self):
        return hasattr(self, 'review') and self.review is not None

class Review(TimeStampedModel):
    
    history      = models.OneToOneField(
        History,
        related_name= 'review',
        verbose_name= 'history',
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
        db_table = 'feature_review'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.history.food.name} | {self.rating}'
