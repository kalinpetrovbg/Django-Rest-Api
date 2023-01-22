from django.contrib import admin

from tweets.models import HackPost


@admin.register(HackPost)
class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "id", "content", "published", "likes")
    readonly_fields = ("likes", "timestamp", "liked_by")
