# DJANGO AXES

# "The number of login attempts allowed before a record is created for the failed logins."
AXES_LOGIN_FAILURE_LIMIT = 3

# "After the number of allowed login attempts are exceeded, should we lock out this IP (and optional user agent)?"
AXES_LOCK_OUT_AT_FAILURE = True

# "If True, lock out / log based on an IP address AND a user agent.
# This means requests from different user agents but from the same IP are treated differently."
AXES_USE_USER_AGENT = False

# "If set, defines a period of inactivity after which old failed login attempts will be forgotten.
#  Can be set to a python timedelta object or an integer. If an integer, will be interpreted as a number of hours."
AXES_COOLOFF_TIME = None

# "If set, specifies a logging mechanism for axes to use. Default: 'axe"
AXES_LOGGER = 'axes.watch_login'

# "If set, specifies a template to render when a user is locked out.
# Template receives cooloff_time and failure_limit as context variables."
AXES_LOCKOUT_TEMPLATE = None

# "If set, specifies a URL to redirect to on lockout.
# If both AXES_LOCKOUT_TEMPLATE and AXES_LOCKOUT_URL are set, the template will be used."
AXES_LOCKOUT_URL = None

# "If True, you’ll see slightly more logging for Axes."
AXES_VERBOSE = True

# "the name of the form field that contains your users usernames."
AXES_USERNAME_FORM_FIELD = 'username'

# "If True prevents to login from IP under particular user if attempts limit exceed,
# otherwise lock out based on IP."
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = False

