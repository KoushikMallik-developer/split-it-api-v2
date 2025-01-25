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
