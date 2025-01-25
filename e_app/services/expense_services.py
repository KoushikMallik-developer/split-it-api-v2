from e_app.export_types.export_expense_types.export_expense import ExportExpense
from e_app.export_types.request_data_types.add_expense_request_type import (
    AddExpenseRequestType,
)
from e_app.serializers.expense_serializer import ExpenseSerializer
from e_app.services.balance_services import BalanceServices


class ExpenseService:

    def add_expense_service(self, data: AddExpenseRequestType):
        expense = ExpenseSerializer().create(data)
        BalanceServices().update_user_group_balance(expense)
        return {
            "message": "Expense added successfully.",
            "expense": ExportExpense(**expense.model_to_dict()),
        }
