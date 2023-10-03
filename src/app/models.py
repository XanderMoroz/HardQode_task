from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Название продукта
    description = models.TextField()  # Описание продукта
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена продукта
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return self.name

class ProductAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Продукт

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Lesson(models.Model):
    title = models.CharField(max_length=100)  # Lesson title
    video_link = models.URLField()  # Video link
    duration = models.PositiveIntegerField()  # Duration in seconds
    products = models.ManyToManyField('Product')  # Products in which the lesson is included

    def __str__(self):
        return self.title

class LessonView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)  # Lesson
    view_time = models.PositiveIntegerField()  # Viewing time in seconds
    status = models.BooleanField(default=False)  # Status "Viewed"/"Not viewed"
    last_view_date = models.DateTimeField(auto_now=True)  # Last view date

    def save(self, *args, **kwargs):
        total_duration = self.lesson.duration
        if self.view_time >= 0.8 * total_duration:
            self.status = True  # Set status as "Viewed"
        else:
            self.status = False  # Set status as "Not viewed"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"