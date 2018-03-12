from django.conf.urls import url
from . import views
urlpatterns = [
  url(r'^$', views.index),
  url(r'^home$', views.home),
  url(r'^login$', views.login),
  url(r'^register$', views.create_user),
  url(r'^search$', views.search),
  url(r'^results$', views.results),
  url(r'^add_to_collection$', views.add_to_collection),
  url(r'^collections/(?P<id>\d+)$', views.view_collection),
  url(r'^collections/(?P<id>\d+)/delete$', views.delete_collection),
  url(r'^slideshow/(?P<id>\d+)$', views.slideshow),
  # url(r'^slideshow/edit/(?P<id>\d+)$', views.index),
  # url(r'^slideshow/delete_slideshow/(?P<id>\d+)$', views.index),
  # url(r'^slideshow/remove_image/(?P<id>\d+)$', views.index),
  url(r'^logout$', views.logout), #clear session

]
