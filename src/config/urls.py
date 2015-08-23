from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from filebrowser.sites import site


admin.autodiscover()


urlpatterns = patterns('',

    # Admin Url
    # (r'^$', RedirectView.as_view(url='/admin/')),

    # Admin Url
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/filebrowser/', include(site.urls)),

    # Auth API
    url(r'^api/', include('administration.urls')),

    # Api docs
    url(r'^docs/', include('rest_framework_swagger.urls')),

    # One app
    url(r'^api/', include('app_one.urls')),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)