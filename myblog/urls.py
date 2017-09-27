from django.conf.urls import url
from myblog import views

urlpatterns = [
    url(r'^post_lc/$', views.Post_lc.as_view(),name='post_lc'),
    url(r'^post_rud/(?P<pk>[0-9]+)/$', views.Post_rud.as_view(),name='post_rud'),
]