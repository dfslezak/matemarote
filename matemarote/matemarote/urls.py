from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import registration
from registration.forms import RegistrationFormUniqueEmail
from django.conf.urls.static import static


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'web_frontend.views.web'),
    
    url(r'^accounts/profile/$', 'web_frontend.views.view_profile'),
    url(r'^accounts/profile/edit$', 'web_frontend.views.edit_profile'),
    url(r'^accounts/register/$', 'registration.views.register',
    {'form_class': RegistrationFormUniqueEmail,
     'backend': 'registration.backends.default.DefaultBackend'},       
     name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('',
    url(r'^games/list/$', 'web_frontend.views.gamelist'),
    url(r'^games/add_game/$', 'web_frontend.views.add_game'),
    url(r'^games/add_game_revision/$', 'web_frontend.views.add_game_revision'),
    url(r'^games/upload/$', 'web_frontend.views.upload_game_revision')
    )


urlpatterns += patterns('',

    url(r'^gameflow/$', 'web_frontend.views.gameflow'),
    url(r'^gameflow/(?P<game_flow_node>.*)/$', 'web_frontend.views.serve_game'),

    #url(r'^(?P<game_name>.*)/login/', game_login, name="game_login"),
    #url(r'^(?P<game_name>.*)/logout/', game_logout, name="game_logout"),
    #url(r'^(?P<game_name>.*)/new_play/', new_play, name="new_play"),
    #url(r'^(?P<game_name>.*)/log_action/', log_action, name="log_action"),
    #url(r'^(?P<game_name>.*)/set_score/', set_score, name="set_score"),
    #url(r'^(?P<game_name>.*)/get_score/', get_score, name="get_score"),
    #url(r'^(?P<game_name>.*)/save_seconds_played/', save_seconds_played, name="save_seconds_played"),
    #url(r'^(?P<game_name>.*)/game_finished/', game_finished, name="game_finished"),
    url(r'^gameflow/(?P<game_flow_node>.*)/res/(?P<resource_path>.*)',
        'web_frontend.views.serve_game_resource', name="serve_game_static"),
    url(r'^gameflow/(?P<game_flow_node>.*)/game_file/(?P<game_file_path>.*)',
        'web_frontend.views.serve_game_file', name="serve_game_file"),
    #url(r'^(?P<game_name>.*)/school_end_stage/', school_end_stage, name="school_end_stage"),
    #url(r'^games/(?P<game_name>.*)/(?P<game_version>.*)/$', 'web_frontend.views.serve_game',
    #    {'page_path':'index.html'}, name="serve_game_index")
    #url(r'^/games/(?P<game_name>.*)/(?P<game_version>.*)/(?P<page_path>.*)',
    #    'web_frontend.views.serve_game_page', name="serve_game_page")        
)
