from django.utils.encoding import force_text
from rest_framework import status


class CheckException(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'
    default_error_slug = 'internal_error'

    def __init__(self, detail=None, error_slug=None):
        if detail is not None:
            self.detail = force_text(detail)
            self.error_slug = force_text(error_slug)
        else:
            self.detail = force_text(self.default_detail)
            self.error_slug = force_text(self.default_error_slug)

    def __str__(self):
        return self.detail


class FriendsExistsException(CheckException):
    def __init__(self):
        self.detail = 'This friend is already added.'

    def __str__(self):
        return repr({'status': 'error', 'message': self.detail})


class FriendAlreadyInvitedException(CheckException):
    def __init__(self):
        self.detail = 'You have already invited this friend, but he does not have an account yet. ' \
                      'Remind him to join One.'

    def __str__(self):
        return repr({'status': 'error', 'message': self.detail})


class UserFriendClashException(CheckException):
    def __init__(self):
        self.detail = "You can't be your own friend, idiot."

    def __str__(self):
        return repr({'status': 'error', 'message': self.detail})


class RemoveUserFriendNotExistException(CheckException):
    def __init__(self):
        self.detail = "You can't remove a friend that is not a friend."

    def __str__(self):
        return repr({'status': 'error', 'message': self.detail})


class InviteRepeatException(CheckException):
    def __init__(self):
        self.detail = "You have already executed this action. Doing it again makes no difference."

    def __str__(self):
        return repr({'status': 'error', 'message': self.detail})


class InviteErrorException(CheckException):
    def __init__(self):
        self.detail = "Something went wrong when trying to invite this friend."

    def __str__(self):
        return repr({'status': 'error', 'message': self.detail})


class FriendRejectedException(CheckException):
    def __init__(self):
        self.detail = "You can't be friends."

    def __str__(self):
        return repr({'status': 'error', 'message': self.detail})


class DontTryLuckException(CheckException):
    def __init__(self):
        self.detail = "You can't try to invite and accept a friend at the same time."

    def __str__(self):
        return repr({'status': 'error', 'message': self.detail})


class APICallError(Exception):
    """API Call failed """
