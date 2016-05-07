AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # default
    'guardian.backends.ObjectPermissionBackend',
)

# DJANGO GUARDIAN
ANONYMOUS_USER_ID = -1