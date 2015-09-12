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
router.register(r'hyper/groups', views.OneGroupHyper)
router.register(r'hyper/user_groups', views.UserGroupHyper)
router.register(r'hyper/group_images', views.GroupImageHyper)
# router.register(r'image/', views.OneImageHyper)
# router.register(r'image/many', views.ImageManyHyper)

# router.register(r'hyper/image_upload', views.ImageUploadHyper)

# URLS
# ---------------------------------------------------------------------------------------------------------------------#
urlpatterns = patterns('',

    # Router fields - API
    url(r'^', include(router.urls)),

                       # Check one per day photo
                       url(r'^one/$', views.CheckOne.as_view()),

    # Group feed
    url(r'^groups/$', views.ListCreateGroups.as_view()),

    # User feed
    url(r'^groups/(?P<group>\d+)/$', views.ListCreateGroupUsers.as_view()),

    # Images feed
                       url(r'^image/(?P<group_list>[0-9,]+)$', views.OneImageHyper.as_view()),
    url(r'^images/$', views.ListImages.as_view()),
    url(r'^images/(?P<group>\d+)/$', views.ListImageGroups.as_view()),

)
