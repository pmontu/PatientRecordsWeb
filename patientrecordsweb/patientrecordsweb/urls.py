from django.conf.urls import patterns, include, url
from patientrecordsweb.views import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    url(r'^$', list),
    (r'^register/$', registerpatient),
    (r'^details/$', details),
    (r'^newvisit/$', newvisit),
    (r'^addcdt/$', addcdt),
    (r'^accounts/login/$',  login),
    (r'^accounts/logout/$', logout),
    (r'^accounts/new/$', newuser),
)
