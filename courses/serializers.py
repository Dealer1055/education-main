from rest_framework import serializers
from .models import CustomUser, Category, Course, VideoContent

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_student', 'is_teacher', 'is_admin']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class VideoContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoContent
        fields = ['id', 'title', 'video_url']

class CourseSerializer(serializers.ModelSerializer):
    videos = VideoContentSerializer(many=True, read_only=True, source='videos')
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'category', 'teacher', 'videos', 'is_subscribed']

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and obj in user.subscribed_courses.all()
