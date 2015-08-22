# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
import logging
logger = logging.getLogger('django')

# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
# shortcuts
from django.shortcuts import render
# contrib.auth
from django.contrib.auth.decorators import login_required
# views.generic
from django.views.generic import DetailView
# 
from .models import *


# GENERIC CLASS BASED VIEWS
# ---------------------------------------------------------------------------------------------------------------------#
class BasicModelView(DetailView):
    model = BasicModel

# CUSTOM VIEWS
# ---------------------------------------------------------------------------------------------------------------------#
@login_required
def about(request):
    # Context variables to pass on to template
    context = {
        'val1': 'Hello',
        'val2': 'World!'
    }

    # Render the template
    return render(request, 'app_name/about_page.html', context)