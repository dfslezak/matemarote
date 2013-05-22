from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import registration
from registration.forms import RegistrationFormUniqueEmail

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'matemarote.views.home', name='home'),
    # url(r'^matemarote/', include('matemarote.foo.urls')),
    url(r'^gameflow/', 'games.views.gameflow'),
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name': 'login_local.html'}),
    #url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'template_name': 'logout.html'}),
    url(r'^$', 'web_frontend.views.web'),

    url(r'^accounts/profile/$', 'web_frontend.views.edit_profile'),
    url(r'^accounts/register/$', 'registration.views.register',
    {'form_class': RegistrationFormUniqueEmail,
     'backend': 'registration.backends.default.DefaultBackend'},       
     name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    #url(r'^accounts/', include('django.contrib.auth.urls')),
    #url(r'', include('django.contrib.auth.urls')),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
)
