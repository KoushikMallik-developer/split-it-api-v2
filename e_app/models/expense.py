from django.db import models

from auth_api.models.base_models.base_model import GenericBaseModel
from auth_api.models.user_models.user import User
from e_app.models.expense_category import ExpenseCategory
from groups.models.group import Group


class Expense(GenericBaseModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="expenses")
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    amount = models.FloatField()
    paid_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="paid_expenses"
    )
    participants = models.ManyToManyField(User, related_name="shared_expenses")
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.category} - {self.amount}"
