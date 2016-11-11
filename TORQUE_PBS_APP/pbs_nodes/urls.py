from django.conf.urls import include, url
from pbs_nodes import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^node/$', views.NodeList.as_view(), name='node-list'),
    url(r'^node/(?P<pk>\w+\-*)/$', views.NodeDetail.as_view(), name='node-detail'),
    url(r'^usercpuperjobspernode/(?P<pk>\w+\-*)/$', views.UserCPUPerJobsPerNode.as_view(), name='usercpuperjobspernode-list'),
    url(r'^npperncpupernode/(?P<pk>\w+\-*)/$', views.NpPerNCPUPerNode.as_view(), name='npperncpupernode-list'),
    url(r'^nodeperstate/$', views.NodePerState.as_view(), name='nodeperstate-list'),
]
urlpatterns = format_suffix_patterns(urlpatterns)