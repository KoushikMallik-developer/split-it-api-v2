from auth_api.models.base_models.base_model import GenericBaseModel
from django.db import models


class FriendRequest(GenericBaseModel):
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Friend Request from {self.sender} to {self.receiver}"
