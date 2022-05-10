from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from user.models import Profile, Record


class UserProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(AuthUserAdmin):
    inlines = [UserProfileInline]

class TimsStampedModelMixinAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

class RecordAdmin(TimsStampedModelMixinAdmin, admin.ModelAdmin):
    pass

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Record, RecordAdmin)
