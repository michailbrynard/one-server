# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
from django.conf.urls import patterns, url, include

import logging
from django.contrib import admin
from rest_framework import routers
from app_one import views

admin.autodiscover()


# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
logger = logging.getLogger('django')


# ROUTERS
# ---------------------------------------------------------------------------------------------------------------------#
router = routers.DefaultRouter()


# URLS
# ---------------------------------------------------------------------------------------------------------------------#
urlpatterns = patterns('',

                       # Router fields - API
                       url(r'^', include(router.urls)),

                       # Check one per day photo
                       url(r'^one/$', views.CheckOne.as_view()),

                       # # Images feed
                       url(r'^image/$', views.CreateImage.as_view()),
                       url(r'^images/$', views.ListImages.as_view()),
                       url(r'^images/(?P<user>\d+)/$$', views.ListUserImages.as_view()),
                       #
                       # # Add snorties
                       # url(r'^snorties/$', views.CreateSnorties.as_view()),
                       #
                       # # List friends and add a friend
                       # url(r'^friends/$', views.ListCreateFriends.as_view()),

                       )
