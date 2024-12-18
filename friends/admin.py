from django.contrib import admin

from friends.models.friend import Friend
from friends.models.friend_request import FriendRequest

admin.site.register(Friend)
admin.site.register(FriendRequest)
