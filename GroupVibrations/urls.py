from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'songs.views.mainIndex'),
    url(r'^songs/', include('songs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)