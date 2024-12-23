from django.contrib import admin
from friends.models.friend import Friend
from friends.models.friend_request import FriendRequest


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    """
    Admin customization for the Friend model.
    """

    list_display = ("user1", "user2", "created_at")
    list_filter = ("user1", "user2")
    search_fields = ("user1__username", "user2__username")


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    """
    Admin customization for the FriendRequest model.
    """

    list_display = ("sender", "receiver", "created_at")
    list_filter = ("sender", "receiver")
    search_fields = ("sender__username", "receiver__username")
