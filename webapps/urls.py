from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ucjobs/', include('ucjobs.urls')),
    url(r'^$', 'ucjobs.views.home'),
    url(r'^$', RedirectView.as_view(url='/webapps/ucjobs/')), # Just for ease of use.
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

