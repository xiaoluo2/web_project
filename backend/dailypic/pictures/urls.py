from django.conf.urls import url
from django.urls import path, include
from pictures.views import PictureViewSet, GalleryViewSet, pull_request
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'pictures', PictureViewSet)
router.register(r'gallerys', GalleryViewSet)
urlpatterns = [
        path('pull_images', pull_request),
        path('', include(router.urls)),
        ]
