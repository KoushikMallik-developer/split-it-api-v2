from django.db import models

from auth_api.models.base_models.base_model import GenericBaseModel
from auth_api.models.user_models.user import User
from groups.models.group import Group


class SettlementTransaction(GenericBaseModel):
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="settlement_transactions"
    )
    settled_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="settled_transactions"
    )
    paid_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="paid_transactions"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Settlement of {self.amount} with {self.paid_to} by {self.settled_by.username}"
