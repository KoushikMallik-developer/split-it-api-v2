import logging
from typing import Optional

from auth_api.auth_exceptions.base_exception import AUTHBaseException


class FriendRequestNotSentError(AUTHBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "Friend Request could not be sent."
        else:
            super().__init__(msg)
        logging.error(self.msg)
