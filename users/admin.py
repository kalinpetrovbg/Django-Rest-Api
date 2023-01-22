from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.safestring import mark_safe

from users.models import CustomUser
from django.contrib.auth import get_user_model


admin.site.site_header = 'HackSoft Admin Portal'
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to HackSoft Admin Portal"
admin.site.unregister(Group)


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    """User admin model."""

    list_display = (
        "email",
        "name",
        "description",
        "own_posts",
        "profile_image"
    )
    readonly_fields = ("token", "date_joined", "last_login")

    exclude = ("groups", "user_permissions")

    actions = ("activate_users",)

    # def activate_users(self, request, queryset):
    #     """Actvate sandboxed users and enable them to log in."""
    #     queryset.update(is_staff=False)

    def profile_image(self, obj: CustomUser) -> bool:
        """Checks if the user has uploaded a photo or not."""
        return True if obj.photo else False
    profile_image.boolean = True

    def own_posts(self, obj: CustomUser) -> str:
        """
        Show a link with all posts by a specific user.
        :param obj: CustomUser
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
