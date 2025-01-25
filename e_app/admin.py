from django.contrib import admin

from e_app.models.balance import Balance
from e_app.models.expense import Expense
from e_app.models.expense_category import ExpenseCategory
from e_app.models.settlement_transaction import SettlementTransaction


admin.site.register(Expense)
admin.site.register(ExpenseCategory)
admin.site.register(Balance)
admin.site.register(SettlementTransaction)
