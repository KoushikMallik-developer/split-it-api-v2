from django.contrib import admin

from auth_api.models.user_models.user import User
from friends.models.friend_model import Friend
from friends.models.friend_request_model import FriendRequest

admin.site.register(User)
admin.site.register(Friend)
admin.site.register(FriendRequest)
