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


class SelfFriendError(AUTHBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "You can't send request to yourself."
        else:
            super().__init__(msg)
        logging.error(self.msg)


class AlreadyFriendRequestSentError(AUTHBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "Friend request already sent."
        else:
            super().__init__(msg)
        logging.error(self.msg)


class ReversedFriendRequestError(AUTHBaseException):
    def __init__(self, receiver_info: Optional[str] = None, msg: Optional[str] = None):
        if not msg and not receiver_info:
            self.msg = f"{receiver_info} has already sent you a friend request."
        elif not receiver_info:
            self.msg = "The user has already sent you a friend request."
        else:
            super().__init__(msg)
        logging.error(self.msg)


class AlreadyAFriendError(AUTHBaseException):
    def __init__(
        self,
        receiver_info: Optional[str] = None,
        msg: Optional[str] = None,
    ):
        if not msg and receiver_info:
            self.msg = f"You are already friends with this {receiver_info}."
        elif not receiver_info:
            self.msg = f"You are already friends."
        else:
            super().__init__(msg)
        logging.error(self.msg)
