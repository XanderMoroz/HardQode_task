from rest_framework import generics

from .models import Lesson, Product, ProductAccess
from .serializers import LessonSerializer, ProductLessonsSerializer, ProductSerializer


# Create your views here.

class LessonListAPIView(generics.ListAPIView):
    """
    Список всех уроков по всем продуктам + статус и время просмотра

    * title - Название урока
    * video_link - Ссылка на видео
    * duration - Длительность в секундах
    * viewed_seconds - Время просмотра урока пользователем в секундах
    * viewed_status - Статус просмотра
    * products - Список курсов в состав которых входит урок
    """
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        products = Product.objects.filter(owner=user)
        return Lesson.objects.filter(products__in=products)

class LessonDetailAPIView(generics.ListAPIView):
    """
    Список уроков по конкретному продукту к которому пользователь имеет доступ

    * title - Название урока
    * video_link - Ссылка на видео
    * duration - Длительность в секундах
    * viewed_seconds - Время просмотра урока пользователем в секундах
    * viewed_status - Статус просмотра
    * last_view_date - Время последнего посещения
    """
    serializer_class = ProductLessonsSerializer


    def get_queryset(self):
        product_id = self.kwargs['pk']
        print(product_id)
        user = self.request.user
        if ProductAccess.objects.filter(user=user, product_id=product_id).exists():
            return Lesson.objects.filter(products__id=product_id)
        return Lesson.objects.none()

class ProductStatisticsAPIView(generics.ListAPIView):
    """
    Список всех продуктов на платформе, с подробной информацией

    * name - Название продукта (учебного курса)
    * lesson_view_count - Количество просмотренных уроков от всех учеников
    * total_view_time - Сумма времени просмотра роликов на курсе всеми учениками
    * total_students - Количество учеников занимающихся на продукте
    * acquisition_percentage - Процент приобретения продукта (учебного курса)
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        products = Product.objects.all()
        return products