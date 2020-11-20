from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from pictures import views

urlpatterns = [
    path('pictures/', views.task_list),
    path('pictures/<int:pk>', views.task_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
