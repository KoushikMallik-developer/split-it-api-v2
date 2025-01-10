import logging
from typing import Optional

from auth_api.auth_exceptions.base_exception import AUTHBaseException


class GroupNotCreatedError(AUTHBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "Group creation failed"
        else:
            super().__init__(msg)
        logging.error(self.msg)


class MemberNotAddedError(AUTHBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "Members not added"
        else:
            super().__init__(msg)
        logging.error(self.msg)


class GroupNotFoundError(AUTHBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "Group does not exists."
        else:
            super().__init__(msg)
        logging.error(self.msg)


class UserAlreadyInGroupError(AUTHBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "User already exists in the group."
        else:
            super().__init__(msg)
        logging.error(self.msg)


class NotAnGroupAdminError(AUTHBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "You are not an admin of this group."
        else:
            super().__init__(msg)
        logging.error(self.msg)
