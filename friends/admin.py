from django.contrib import admin
from friends.models.friend_request import FriendRequest


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    """
    Admin customization for the FriendRequest model.
    """

    list_display = ("sender", "receiver", "created_at")
    list_filter = ("sender", "receiver")
    search_fields = ("sender__username", "receiver__username")
