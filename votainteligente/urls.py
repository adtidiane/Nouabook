from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'votainteligente.views.home', name='home'),
    # url(r'^votainteligente/', include('votainteligente.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    #url(r'^', include('elections.urls')),
    #('^pages/', include('flatpages_i18n.urls')),#('^pages/', include('django.contrib.flatpages.urls')),
    #(r'^tinymce/', include('tinymce.urls')),
)

# these urls are used with i18n
urlpatterns += i18n_patterns('',
    url(r'^', include('elections.urls')),
    url(r'^page', include('flatpages_i18n.urls')),
    (r'^tinymce/', include('tinymce.urls')),
)