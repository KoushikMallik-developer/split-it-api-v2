from _decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from auth_api.auth_exceptions.user_exceptions import UserNotFoundError
from auth_api.models.user_models.user import User
from e_app.models.settlement_transaction import SettlementTransaction
from groups.group_exceptions.group_exceptions import GroupNotFoundError
from groups.models.group import Group


class SettlementSerializer(serializers.ModelSerializer):

    def validate(self, data) -> dict:
        group = None
        settled_by = None
        paid_to = None

        try:
            if data.get("group_id") and isinstance(data.get("group_id"), str):
                group = Group.objects.get(id=data.get("group_id"))
        except ObjectDoesNotExist:
            raise GroupNotFoundError()

        try:
            if data.get("settled_by") and isinstance(data.get("settled_by"), str):
                settled_by = User.objects.get(id=data.get("settled_by"))
        except ObjectDoesNotExist:
            raise UserNotFoundError("Specified user is not found.")

        try:
            if data.get("paid_to") and isinstance(data.get("paid_to"), str):
                paid_to = User.objects.get(id=data.get("paid_to"))
        except ObjectDoesNotExist:
            raise UserNotFoundError("Specified user is not found.")

        if not data.get("amount") or not isinstance(data.get("amount"), Decimal):
            raise ValueError("Amount is required.")

        return {
            "group": group,
            "settled_by": settled_by,
            "paid_to": paid_to,
            "amount": data.get("amount"),
        }

    def create(self, data) -> SettlementTransaction:
        validated_data = self.validate(data)
        settlement = SettlementTransaction(
            group=validated_data.get("group"),
            settled_by=validated_data.get("settled_by"),
            paid_to=validated_data.get("paid_to"),
            amount=validated_data.get("amount"),
        )
        settlement.save()
        return settlement
