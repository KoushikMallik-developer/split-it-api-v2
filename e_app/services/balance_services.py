from e_app.models.balance import Balance
from e_app.models.expense import Expense


class BalanceServices:

    @staticmethod
    def update_user_group_balance(expense: Expense):
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

    @staticmethod
    def update_user_group_balance_on_delete(expense: Expense):
        balance = Balance.objects.get(
            user__id=expense.paid_by.id, group__id=expense.group.id
        )  # handling user group balance for paid by
        balance.amount -= expense.amount
        expense.paid_by.balance -= expense.amount  # User Personal ultimate balance
        expense.paid_by.save()
        balance.save()

        # handling user group balance for participants
        for participant in expense.participants.all():
            balance = Balance.objects.get(
                user__id=participant.id, group__id=expense.group.id
            )
            balance.amount += expense.amount / len(expense.participants.all())
            participant.balance += expense.amount / len(expense.participants.all())
            participant.save()
            balance.save()

    @staticmethod
    def update_user_group_balance_on_settlement(settlement):
        balance = Balance.objects.get(
            user__id=settlement.settled_by.id, group__id=settlement.group.id
        )
        balance.amount += settlement.amount
        settlement.settled_by.balance += settlement.amount
        settlement.settled_by.save()
        balance.save()

        balance = Balance.objects.get(
            user__id=settlement.paid_to.id, group__id=settlement.group.id
        )
        balance.amount -= settlement.amount
        settlement.paid_to.balance -= settlement.amount
        settlement.paid_to.save()
        balance.save()

    @staticmethod
    def update_user_group_balance_on_settlement_delete(settlement):
        balance = Balance.objects.get(
            user__id=settlement.settled_by.id, group__id=settlement.group.id
        )
        balance.amount -= settlement.amount
        settlement.settled_by.balance -= settlement.amount
        settlement.settled_by.save()
        balance.save()

        balance = Balance.objects.get(
            user__id=settlement.paid_to.id, group__id=settlement.group.id
        )
        balance.amount += settlement.amount
        settlement.paid_to.balance += settlement.amount
        settlement.paid_to.save()
        balance.save()

    @staticmethod
    def update_group_total_spent(expense: Expense):
        group = expense.group
        group.total_spent += expense.amount
        group.save()
