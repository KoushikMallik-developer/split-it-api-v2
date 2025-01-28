from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from e_app.expense_exceptions.expense_exceptions import (
    SettlementNotFoundError,
    NotAParticipantError,
)
from e_app.export_types.export_expense_types.export_settlement import (
    ExportSettlement,
    ExportSettlementList,
)
from e_app.export_types.request_data_types.add_settlement_request_type import (
    AddSettlementRequestType,
)
from e_app.export_types.request_data_types.get_group_settlements_request_type import (
    GetGroupSettlementsRequestType,
)
from e_app.export_types.request_data_types.remove_settlement_request_type import (
    RemoveSettlementRequestType,
)
from e_app.models.settlement_transaction import SettlementTransaction
from e_app.serializers.settlement_serializer import SettlementSerializer
from e_app.services.balance_services import BalanceServices


class SettlementService:
    def add_settlement(self, data: AddSettlementRequestType):
        settlement: SettlementTransaction = SettlementSerializer().create(
            data=data.dict()
        )
        BalanceServices.update_user_group_balance_on_settlement(settlement=settlement)
        return {
            "message": "Settlement added successfully",
            "settlement": ExportSettlement(**settlement.model_to_dict()),
        }

    def remove_settlement(self, data: RemoveSettlementRequestType, uid: str):
        try:
            settlement = SettlementTransaction.objects.get(
                id=data.settlement_id, is_deleted=False
            )
            if (
                str(settlement.settled_by.id) != uid
                and str(settlement.paid_to.id) != uid
            ):
                raise NotAParticipantError()
            BalanceServices.update_user_group_balance_on_settlement_delete(
                settlement=settlement
            )
            settlement.delete()
            return {"message": "Settlement removed successfully"}
        except ObjectDoesNotExist:
            raise SettlementNotFoundError()

    def get_all_settlements(self, uid: str) -> dict:
        settlements = SettlementTransaction.objects.filter(
            Q(settled_by__id=uid) or Q(paid_by__id=uid), is_deleted=False
        )
        return {
            "data": ExportSettlementList(
                settlements=[
                    ExportSettlement(**settlement.model_to_dict())
                    for settlement in settlements
                ]
            ).model_dump(),
            "message": "Settlements fetched successfully",
        }

    def get_group_settlements(self, data: GetGroupSettlementsRequestType):
        settlements = SettlementTransaction.objects.filter(
            group__id=data.group_id, is_deleted=False
        )
        return {
            "data": ExportSettlementList(
                settlements=[
                    ExportSettlement(**settlement.model_to_dict())
                    for settlement in settlements
                ]
            ).model_dump(),
            "message": "Settlements fetched successfully",
        }

    def get_group_settlements_by_user(
        self, data: GetGroupSettlementsRequestType, uid: str
    ):
        settlements = SettlementTransaction.objects.filter(
            group__id=data.group_id, is_deleted=False, settled_by__id=uid
        )
        return {
            "data": ExportSettlementList(
                settlements=[
                    ExportSettlement(**settlement.model_to_dict())
                    for settlement in settlements
                ]
            ).model_dump(),
            "message": "Settlements fetched successfully",
        }
