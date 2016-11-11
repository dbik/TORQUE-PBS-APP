from django.conf.urls import include, url
from pbs_queues import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.QueueList.as_view(), name='queues-list'),
    url(r'^userqueue/$', views.UserQueues.as_view(), name='userqueue-list'),
    url(r'^userperalljobsperqueue/(?P<pk>\w+)/$', views.UserPerAllJobsPerQueue.as_view(), name='userperalljobsperqueue-list'),
    url(r'^userjobsperqueueperjobstate/(?P<pk>\w+)/$', views.UserJobsPerQueuePerJobState.as_view(), name='userjobsperqueueperjobstate-list'),
    url(r'^alljobsperqueueperjobstate/(?P<pk>\w+)/$', views.AllJobsPerQueuePerJobState.as_view(), name='alljobsperqueueperjobstate-list'),
    url(r'^queue/(?P<pk>\w+)/$', views.QueueDetail.as_view(), name='queue-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)