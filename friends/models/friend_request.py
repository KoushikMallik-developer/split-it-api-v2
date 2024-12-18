from auth_api.models.base_models.base_model import GenericBaseModel
from django.db import models

from auth_api.models.user_models.user import User


class FriendRequest(GenericBaseModel):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"
