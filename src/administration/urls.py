# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
# conf.urls
from django.contrib import admin
from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from administration import views
from rest_framework import routers

admin.autodiscover()


# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
import logging

logger = logging.getLogger('django')


# ROUTERS
# ---------------------------------------------------------------------------------------------------------------------#
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)


# URLS
# ---------------------------------------------------------------------------------------------------------------------#
urlpatterns = patterns('',
    # Static views
    url(r'^grappelli/', include('grappelli.urls')),

    # Default auth
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^api-token-verify/', 'rest_framework_jwt.views.verify_jwt_token'),

    # URLs for registering
    url(r'^register/$', views.Register.as_view(), name='rest_register'),
    url(r'^account-confirm-email/(?P<key>\w+)/$', TemplateView.as_view(),
        name='account_confirm_email'),
    url(r'^verify-email/$', views.VerifyEmail.as_view(), name='rest_verify_email'),

    # URLs that do not require a session or valid token
    url(r'^password/reset/$', views.PasswordReset.as_view(),
        name='rest_password_reset'),
    url(r'^password/reset/confirm/$', views.PasswordResetConfirm.as_view(),
        name='rest_password_reset_confirm'),
    url(r'^login/$', views.Login.as_view(), name='rest_login'),

    # URLs that require a user to be logged in with a valid session / token.
    url(r'^logout/$', views.Logout.as_view(), name='rest_logout'),
    # url(r'^user/$', views.UserDetails.as_view(), name='rest_user_details'),
    url(r'^password/change/$', views.PasswordChange.as_view(),
        name='rest_password_change'),

    # this url is used to generate email content
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'),

    # Router fields - API
    url(r'^', include(router.urls)),
)