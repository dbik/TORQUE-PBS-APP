from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

import views

urlpatterns = [

    url(r'^register/$', views.CustomUserRegistration.as_view(), name='custom-user-registration'),
    url(r'^$', views.CustomUserList.as_view(), name='custom-user-list'),
    url(r'^(?P<pk>[0-9]+)/$', views.CustomUserDetail.as_view(), name='custom-user-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
