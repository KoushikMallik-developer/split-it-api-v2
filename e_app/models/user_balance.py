from django.db import models

from auth_api.models.base_models.base_model import GenericBaseModel
from auth_api.models.user_models.user import User


class UserBalance(GenericBaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_balances"
    )
    amount = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username}: {self.amount}"
