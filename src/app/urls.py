from django.urls import path
from .views import LessonListAPIView, LessonDetailAPIView, ProductStatisticsAPIView

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('product/<int:pk>/', LessonDetailAPIView.as_view(), name='product_lessons'),
    path('statistics/', ProductStatisticsAPIView.as_view(), name='product-statistics'),
]