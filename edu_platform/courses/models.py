# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # Kurslarga obuna bo‘lganlar (ko‘p-ko‘pga)
    subscribed_courses = models.ManyToManyField(
        'Course',
        related_name='subscribers',
        blank=True
    )


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    # O'qituvchi bilan aloqasi
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='teaching_courses'
    )
    
    # Talabalar bilan ko‘p-ko‘pga aloqasi
    students = models.ManyToManyField(
        CustomUser,
        related_name='enrolled_courses',
        blank=True
    )

    def __str__(self):
        return self.title


class VideoContent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    video_url = models.URLField()

    def __str__(self):
        return self.title
