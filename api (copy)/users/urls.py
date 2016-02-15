from django.conf.urls import url, include
from rest_framework import routers
from users import views

#~ router = routers.DefaultRouter()
#~ router.register(r'users', views.UserViewSet)
#~ router.register(r'groups', views.GroupViewSet)
app_name = 'users'
urlpatterns = [
    url(r'^create/$', views.create, name = 'create'),
    url(r'^index/$', views.index),
    #url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace = 'rest_framework'))
]

