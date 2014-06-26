from django.conf.urls import patterns, include, url
from django.contrib import admin
from photos import views, api

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.HomeView.as_view()),
    url(r'^photos/$',views.PhotoListView.as_view()),
    url(r'^photos/(?P<pk>[0-9]+)$',views.PhotoDetailView.as_view()),
    url(r'^login$',views.UserLoginView.as_view()),
    url(r'^logout',views.UserLogout.as_view()),
    url(r'^user_profile',views.UserProfileView.as_view()),
    url(r'^create','photos.views.create_photo'),

    # User API urls
    url(r'api/1.0/users/$', api.UserListAPI.as_view()),
    url(r'api/1.0/users/(?P<pk>[0-9]+)$', api.UserDetailAPI.as_view()),

    # Photo API urls
    url(r'api/1.0/photos/$', api.PhotoListAPI.as_view()),
    url(r'api/1.0/photos/(?P<pk>[0-9]+)$', api.PhotoDetailAPI.as_view())
)
