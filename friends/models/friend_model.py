from auth_api.models.base_models.base_model import GenericBaseModel
from django.db import models


class Friend(GenericBaseModel):
    user1 = models.CharField(max_length=100)
    user2 = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"u1-{self.user1}/u2-{self.user2}"
