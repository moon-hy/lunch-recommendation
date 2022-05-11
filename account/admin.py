from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from account.models import Profile


class UserProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(AuthUserAdmin):
    inlines = [UserProfileInline]

class TimsStampedModelMixinAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
