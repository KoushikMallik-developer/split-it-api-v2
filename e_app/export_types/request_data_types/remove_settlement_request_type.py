from pydantic import BaseModel


class RemoveSettlementRequestType(BaseModel):
    settlement_id: str
