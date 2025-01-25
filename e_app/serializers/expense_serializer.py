from rest_framework.serializers import Serializer

from auth_api.models.user_models.user import User
from e_app.models.expense import Expense
from e_app.models.expense_category import ExpenseCategory
from groups.models.group import Group


class ExpenseSerializer(Serializer):
    def validate(self, data):
        if not data.get("paid_by"):
            raise ValueError("Paid by user is required.")

        if not data.get("participants"):
            raise ValueError("Participants are required.")

        if not data.get("category"):
            raise ValueError("Category is required.")

        if not data.get("group_id"):
            raise ValueError("Group ID is required.")

        if not data.get("name"):
            raise ValueError("Name is required.")

        if not data.get("amount"):
            raise ValueError("Amount is required.")

        if data.get("amount") <= 0:
            raise ValueError("Amount must be greater than zero.")

        group = Group.objects.get(id=data.get("group_id"))
        if not group:
            raise ValueError("Group is not a valid group.")

        participants = []
        for participant_id in data.get("participants"):
            if not isinstance(participant_id, str):
                raise ValueError("Participants must be a list of strings.")
            participant = User.objects.get(id=participant_id)
            if not participant:
                raise ValueError("Participant is not a valid user.")
            if not group.members.filter(id=participant.id).exists():
                raise ValueError("Participant is not a member of the group.")
            participants.append(participant)

        paid_by = User.objects.get(id=data.get("paid_by"))
        if not paid_by:
            raise ValueError("Paid by user is not a valid user.")

        if not group.members.filter(id=paid_by.id).exists():
            raise ValueError("Paid by user is not a member of the group.")

        category = ExpenseCategory.objects.get(name=data.get("category").lower())
        if not category:
            raise ValueError("Category is not a valid category.")

        data["participants"] = participants
        data["group"] = group
        data["paid_by"] = paid_by
        data["category"] = category

        return data

    def create(self, data):
        if self.validate(data):
            expense_data = {
                "name": data.get("name"),
                "amount": data.get("amount"),
                "paid_by": data.get("paid_by"),
                "category": data.get("category"),
                "group": data.get("group"),
            }
            expense = Expense.objects.create(**expense_data)
            expense.participants.set(data.get("participants"))

            expense.save()
            return expense
