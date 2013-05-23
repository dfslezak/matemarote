from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import registration
from registration.forms import RegistrationFormUniqueEmail
from django.conf.urls.static import static


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^gameflow/', 'games.views.gameflow'),
    url(r'^$', 'web_frontend.views.web'),

    url(r'^accounts/profile/$', 'web_frontend.views.view_profile'),
    url(r'^accounts/profile/edit$', 'web_frontend.views.edit_profile'),
    url(r'^accounts/register/$', 'registration.views.register',
    {'form_class': RegistrationFormUniqueEmail,
     'backend': 'registration.backends.default.DefaultBackend'},       
     name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)