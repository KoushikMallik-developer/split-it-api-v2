from django.urls import path

from e_app.views.add_expense import AddExpense

urlpatterns = [
    path("add-expense/", AddExpense.as_view(), name="add-expense"),
]
