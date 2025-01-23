from auth_api.models.base_models.base_model import GenericBaseModel
from django.db import models

from auth_api.models.user_models.user import User


class Group(GenericBaseModel):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name="members")
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True, default="")
    image = models.CharField(max_length=500, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
