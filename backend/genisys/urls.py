from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
#from django_cas_ng import views as cas_views

API_TITLE = 'Genisys API'
API_DESCRIPTION = 'Genisys Assessment Platform API'

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^api/', include('api.urls')),
    url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    url(r'^docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),
#    url(r'^accounts/login$', cas_views.login, name='cas_ng_login'),
#    url(r'^accounts/logout$', cas_views.logout, name='cas_ng_logout'),
#    url(r'^accounts/callback$', cas_views.callback, name='cas_ng_proxy_callback')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
