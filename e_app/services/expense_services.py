from django.core.exceptions import ObjectDoesNotExist

from e_app.expense_exceptions.expense_exceptions import (
    ExpenseNotFoundError,
    NotAParticipantError,
)
from e_app.export_types.export_expense_types.export_expense import ExportExpense
from e_app.export_types.request_data_types.add_expense_request_type import (
    AddExpenseRequestType,
)
from e_app.export_types.request_data_types.get_group_expense_request_type import (
    GetGroupExpenseRequestType,
)
from e_app.export_types.request_data_types.remove_expense_request_type import (
    RemoveExpenseRequestType,
)
from e_app.models.expense import Expense
from e_app.serializers.expense_serializer import ExpenseSerializer
from e_app.services.balance_services import BalanceServices
from groups.group_exceptions.group_exceptions import GroupNotFoundError
from groups.models.group import Group


class ExpenseService:

    def add_expense_service(self, data: AddExpenseRequestType) -> dict:
        expense = ExpenseSerializer().create(data.model_dump())
        BalanceServices().update_user_group_balance(expense)
        return {
            "message": "Expense added successfully.",
            "expense": ExportExpense(**expense.model_to_dict()),
        }

    def remove_expense_service(self, data: RemoveExpenseRequestType, uid: str) -> dict:
        try:
            expense = Expense.objects.get(id=data.expense_id, is_deleted=False)
            if (
                expense.group.members.filter(id=uid).exists()
                and expense.participants.filter(id=uid).exists()
            ):
                expense.is_deleted = True
                expense.save()
                BalanceServices().update_user_group_balance_on_delete(expense)
                return {"message": "Expense removed successfully."}
            else:
                raise NotAParticipantError()
        except ObjectDoesNotExist:
            raise ExpenseNotFoundError()

    def get_group_expense_service(
        self, data: GetGroupExpenseRequestType, uid: str
    ) -> list:
        try:
            group = Group.objects.get(id=data.group_id)
            expenses = Expense.objects.filter(group__id=data.group_id, is_deleted=False)
            if group.members.filter(id=uid).exists():
                return [
                    ExportExpense(**expense.model_to_dict()).model_dump()
                    for expense in expenses
                ]
            else:
                raise NotAParticipantError()
        except ObjectDoesNotExist:
            raise GroupNotFoundError()

    def get_all_expenses_service(self, user_id: str):
        expenses = Expense.objects.filter(participants__id=user_id, is_deleted=False)
        return [
            ExportExpense(**expense.model_to_dict()).model_dump()
            for expense in expenses
        ]
