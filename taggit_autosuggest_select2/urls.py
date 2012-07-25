from django.conf.urls.defaults import *


urlpatterns = patterns('taggit_autosuggest_select2.views',
    url(r'^list/$', 'list_tags', name='taggit_autosuggest_select2-list'),
    url(r'^list_all.json', 'list_all_tags', name='taggit_autosuggest_select2-list-all'),
)
