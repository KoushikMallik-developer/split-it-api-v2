import logging
from typing import Optional

from auth_api.auth_exceptions.base_exception import AUTHBaseException


class ExpenseNotFoundError(AUTHBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "Expense not found."
        else:
            super().__init__(msg)
        logging.error(self.msg)


class NotAParticipantError(AUTHBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "You are not a participant of this expense."
        else:
            super().__init__(msg)
        logging.error(self.msg)


class SettlementNotFoundError(AUTHBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "Settlement not found."
        else:
            super().__init__(msg)
        logging.error(self.msg)
