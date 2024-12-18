from auth_api.models.base_models.base_model import GenericBaseModel
from django.db import models

from auth_api.models.user_models.user import User


class Friend(GenericBaseModel):
    user1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friends_initiated"
    )
    user2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friends_received"
    )

    def save(self, *args, **kwargs):
        # if Friend.objects.filter(user1=self.user1, user2=self.user2).exists():
        #     raise ValueError("This friendship already exists.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"u1-{self.user1}/u2-{self.user2}"
