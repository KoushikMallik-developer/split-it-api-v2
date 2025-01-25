from django.urls import path

from e_app.views.add_expense import AddExpense
from e_app.views.get_all_groups import GetAllExpenses
from e_app.views.get_group_expenses import GetGroupExpenses
from e_app.views.remove_expense import RemoveExpense

urlpatterns = [
    path("add-expense/", AddExpense.as_view(), name="add-expense"),
    path("remove-expense/", RemoveExpense.as_view(), name="remove-expense"),
    path("get-group-expenses/", GetGroupExpenses.as_view(), name="get-group-expense"),
    path("get-all-expenses/", GetAllExpenses.as_view(), name="get-all-expense"),
]
