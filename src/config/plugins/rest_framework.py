import datetime

ANONYMOUS_USER_ID = -1

# REST FRAMEWORK ~ http://www.django-rest-framework.org/
# ---------------------------------------------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'PAGINATE_BY': 20
}

# JWT Token
# ---------------------------------------------------------------------------------------------------------------------
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=31104000),
}

SESSION_COOKIE_AGE = 1209600*5
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

CORS_ORIGIN_ALLOW_ALL = True
