from django.contrib import admin

from friends.models.friend_model import Friend
from friends.models.friend_request_model import FriendRequest

admin.site.register(Friend)
admin.site.register(FriendRequest)
