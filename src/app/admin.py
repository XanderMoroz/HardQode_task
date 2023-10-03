from django.contrib import admin
from .models import Lesson, LessonView, Product, ProductAccess

# Register your models here.

# Подключаем к админке учебный курс
admin.site.register(Product)
# Подключаем к админке доступы к учебному курсу для учеников
admin.site.register(ProductAccess)
# Подключаем к админке уроки
admin.site.register(Lesson)
# Подключаем к админке просмотры уроков
admin.site.register(LessonView)
