from django.urls import path

from e_app.views.add_expense import AddExpense
from e_app.views.add_settlement import AddSettlement
from e_app.views.get_all_expenses import GetAllExpenses
from e_app.views.get_all_settlements import GetAllSettlements
from e_app.views.get_group_expenses import GetGroupExpenses
from e_app.views.get_group_settlements import GetGroupSettlements
from e_app.views.get_group_settlements_by_user_id import GetGroupSettlementsByUserId
from e_app.views.remove_expense import RemoveExpense
from e_app.views.remove_settlement import RemoveSettlement

urlpatterns = [
    path("add-expense/", AddExpense.as_view(), name="add-expense"),
    path("remove-expense/", RemoveExpense.as_view(), name="remove-expense"),
    path("get-group-expenses/", GetGroupExpenses.as_view(), name="get-group-expense"),
    path("get-all-expenses/", GetAllExpenses.as_view(), name="get-all-expense"),
    path("add-settlement/", AddSettlement.as_view(), name="add-settlement"),
    path("remove-settlement/", RemoveSettlement.as_view(), name="remove-settlement"),
    path(
        "get-all-settlements/", GetAllSettlements.as_view(), name="get-all-settlements"
    ),
    path(
        "get-group-settlements/",
        GetGroupSettlements.as_view(),
        name="get-group-settlements",
    ),
    path(
        "get-group-settlements-by-user-id/",
        GetGroupSettlementsByUserId.as_view(),
        name="get-group-settlements-by-user-id",
    ),
]
