from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from user.models import Profile


class UserProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(AuthUserAdmin):
    inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
