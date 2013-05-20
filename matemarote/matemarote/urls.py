from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'matemarote.views.home', name='home'),
    # url(r'^matemarote/', include('matemarote.foo.urls')),
    url(r'^gameflow/', 'games.views.gameflow'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name': 'login_local.html'}),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
)
