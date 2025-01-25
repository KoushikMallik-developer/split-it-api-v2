from django.db import models

from auth_api.models.base_models.base_model import GenericBaseModel
from auth_api.models.user_models.user import User
from e_app.models.expense_category import ExpenseCategory
from groups.models.group import Group


class Expense(GenericBaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="expenses")
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="paid_expenses"
    )
    participants = models.ManyToManyField(User, related_name="shared_expenses")
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.category} - {self.amount}"
