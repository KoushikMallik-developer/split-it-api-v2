from e_app.models.balance import Balance
from e_app.models.expense import Expense


class BalanceServices:

    def update_user_group_balance(self, expense: Expense):
        # handling user group balance for paid by
        if not Balance.objects.filter(
            user__id=expense.paid_by.id, group__id=expense.group.id
        ).exists():
            balance = Balance.objects.create(user=expense.paid_by, group=expense.group)
            balance.save()
        balance = Balance.objects.get(
            user__id=expense.paid_by.id, group__id=expense.group.id
        )
        balance.amount += expense.amount
        expense.paid_by.balance += expense.amount  # User Personal ultimate balance
        expense.paid_by.save()
        balance.save()

        # handling user group balance for participants
        for participant in expense.participants.all():
            if not Balance.objects.filter(
                user__id=participant.id, group__id=expense.group.id
            ).exists():
                balance = Balance.objects.create(user=participant, group=expense.group)
                balance.save()
            else:
                balance = Balance.objects.get(
                    user__id=participant.id, group__id=expense.group.id
                )
            balance.amount -= expense.amount / len(expense.participants.all())
            participant.balance -= expense.amount / len(expense.participants.all())
            participant.save()
            balance.save()
