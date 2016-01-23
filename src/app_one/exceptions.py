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
        self.detail = 'You have already invited this friend, but he doe snot have an account yet. Tell him to join One.'

    def __str__(self):
        return repr({'status': 'error', 'message': self.detail})


class UserFriendClashException(CheckException):
    def __init__(self):
        self.detail = "You can't be your own friend, idiot."

    def __str__(self):
        return repr({'status': 'error', 'message': self.detail})


class APICallError(Exception):
    """API Call failed """
