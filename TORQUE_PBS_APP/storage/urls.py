from django.conf.urls import url
from storage import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.FileList.as_view(), name='file-list'),
    url(r'^(?P<pk>[0-9]+)/$', views.FileDetail.as_view(), name='file-detail'),
    #url(r'^file/(?P<pk>[0-9]+)$', views.file_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)