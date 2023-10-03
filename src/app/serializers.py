from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework import serializers
from .models import Lesson, LessonView, Product, ProductAccess


class LessonSerializer(serializers.ModelSerializer):
    viewed_seconds = serializers.SerializerMethodField()
    viewed_status = serializers.SerializerMethodField()

    def get_viewed_seconds(self, obj):
        lesson_view = LessonView.objects.filter(
            lesson=obj).first()
        if lesson_view:
            return lesson_view.view_time
        return None

    def get_viewed_status(self, obj):
        lesson_view = LessonView.objects.filter(
            lesson=obj).first()
        if lesson_view:
            return lesson_view.status
        return None

    class Meta:
        model = Lesson
        fields = ['title',
                  'video_link',
                  'duration',
                  'viewed_seconds',
                  'viewed_status',
                  'products']


class ProductLessonsSerializer(serializers.ModelSerializer):
    viewed_seconds = serializers.SerializerMethodField()
    viewed_status = serializers.SerializerMethodField()
    last_view_date = serializers.SerializerMethodField()

    def get_viewed_seconds(self, obj):
        lesson_view = LessonView.objects.filter(
            lesson=obj).first()
        if lesson_view:
            return lesson_view.view_time
        return "Current user didn't see the lesson"

    def get_viewed_status(self, obj):
        lesson_view = LessonView.objects.filter(
            lesson=obj).first()
        if lesson_view:
            return lesson_view.status
        return False

    def get_last_view_date(self, obj):
        lesson_view = LessonView.objects.filter(
            lesson=obj).first()
        if lesson_view:
            return lesson_view.last_view_date
        return None

    class Meta:
        model = Lesson
        fields = ['title',
                  'video_link',
                  'duration',
                  'viewed_seconds',
                  'viewed_status',
                  'last_view_date']


class ProductSerializer(serializers.ModelSerializer):
    lesson_view_count = serializers.SerializerMethodField()
    total_view_time = serializers.SerializerMethodField()
    total_students = serializers.SerializerMethodField()
    acquisition_percentage = serializers.SerializerMethodField()

    def get_lesson_view_count(self, obj):
        count = LessonView.objects.filter(
            lesson__products__id=obj.id,
            status=True).count()
        if count:
            return count
        return "Этот курс еще никто не видел"

    def get_total_view_time(self, obj):
        total_view_time = (LessonView.objects.filter(
            lesson__products__id=obj.id
        ).aggregate(
            Sum('view_time')))

        if total_view_time['view_time__sum']:
            return total_view_time['view_time__sum']
        return 'Этот курс не смотрели ни секунды'

    def get_total_students(self, obj):
        total_student = ProductAccess.objects.filter(
            product__id=obj.id).values('user').count()
        if total_student:
            return total_student
        return "Никто не получил доступ на курс"

    def get_acquisition_percentage(self, obj):
        access_count = ProductAccess.objects.filter(product__id=obj.id).values('user').count()
        total_users = User.objects.all().count()
        percentage = (access_count / total_users) * 100
        return percentage

    class Meta:
        model = Product
        fields = ['name', 'lesson_view_count', 'total_view_time', 'total_students', 'acquisition_percentage']