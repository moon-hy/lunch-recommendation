from django.contrib import admin

from post.models import Post, Comment


class TimsStampedModelMixinAdmin(admin.ModelAdmin):
    readonly_fields = (
        'created_at',
    )

class PostAdmin(TimsStampedModelMixinAdmin, admin.ModelAdmin):
    pass

class CommentAdmin(TimsStampedModelMixinAdmin, admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
