from django.db import models
from auth_api.models.user_models.user import User
from groups.models.group import Group


class SettlementTransaction(models.Model):
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="settlement_transactions"
    )
    settled_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="settled_transactions"
    )
    paid_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="paid_transactions"
    )
    amount = models.FloatField()
    settled_on = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Settlement of {self.amount} for {self.expense} by {self.settled_by.username}"
