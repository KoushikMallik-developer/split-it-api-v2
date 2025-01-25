from django.db import models

from auth_api.models.base_models.base_model import GenericBaseModel
from auth_api.models.user_models.user import User
from groups.models.group import Group


class Balance(GenericBaseModel):
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="balances_group"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="balances_user"
    )
    amount = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username}: {self.amount} in {self.group.name}"
