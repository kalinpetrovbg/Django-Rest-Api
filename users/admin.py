from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from users.models import HackUser


admin.site.site_header = 'Hack Soft Admin Portal'
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to Hack Soft Admin Portal"
admin.site.unregister(Group)


@admin.register(HackUser)
class UserAdmin(admin.ModelAdmin):
    """User admin model."""

    list_display = (
        "username",
        "email",
        "password",
        "name",
        "description",
        "own_posts",
        "profile_image"
    )
    readonly_fields = ("token", "registered")

    def profile_image(self, obj: HackUser) -> bool:
        """Checks if the user has uploaded a photo or not."""
        return True if obj.photo else False
    profile_image.boolean = True

    def own_posts(self, obj: HackUser) -> str:
        """
        Show a link with all posts by a specific user.
        :param obj: HackUser
        :return: Clickable string
        """
        count = obj.hackpost_set.count()
        url = (
            reverse("admin:tweets_hackpost_changelist")
            + "?"
            + urlencode({"author__id__exact": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Posts</a>', url, count)

    own_posts.short_description = "Posts"
