from django.contrib import admin

from feature.models import (
    Category, 
    Food, 
    History,
    Review
)


admin.site.register(Category)
admin.site.register(Food)
admin.site.register(History)
admin.site.register(Review)
