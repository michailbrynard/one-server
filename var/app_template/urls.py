# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
import logging
logger = logging.getLogger('django')


# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
# conf.urls
from django.conf.urls import patterns, url

# contrib.auth
from django.contrib.auth.decorators import login_required

# 
from . import views


# URLS
# ---------------------------------------------------------------------------------------------------------------------#
urlpatterns = patterns('',
    # Static views

    # Generic class based views
    url(r'basic_model/(?P<pk>[0-9]+)/$', login_required(views.BasicModelView.as_view()),
        name='basic_model_detail'),

    # Custom views
    url(r'/$', '.views.about', name='about'),
)