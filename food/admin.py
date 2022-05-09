from django.contrib import admin

from food.models import (
    Tag, Category, Food, Review
)


admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Food)
admin.site.register(Review)
