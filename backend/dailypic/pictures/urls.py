from django.conf.urls import url
from django.urls import path, include
from pictures.views import PictureViewSet, GalleryViewSet 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'pictures', PictureViewSet)
router.register(r'gallerys', GalleryViewSet)
urlpatterns = router.urls
