from django.conf.urls import url
from django.urls import path, include
from account.views import RegisterApi, UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet())
urlpatterns = [
      path('register', RegisterApi.as_view()),
      include('', include(router.urls)),
]
