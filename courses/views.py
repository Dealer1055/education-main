# courses/views.py

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth import get_user_model
from .models import Category, Course, VideoContent, CustomUser
from .serializers import CategorySerializer, CourseSerializer, VideoContentSerializer, UserSerializer
from .permissions import IsTeacherOrReadOnly, IsOwnerOrReadOnly

User = get_user_model()

# -------------------- Category --------------------
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# -------------------- Course --------------------
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        course = self.get_object()
        user = request.user
        course.students.add(user)
        user.subscribed_courses.add(course)
        return Response({'status': 'subscribed'})

# -------------------- Video --------------------
class VideoContentViewSet(viewsets.ModelViewSet):
    queryset = VideoContent.objects.all()
    serializer_class = VideoContentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        if course.teacher != self.request.user:
            raise PermissionDenied("Siz faqat o'zingiz yaratgan kursga video qo‘sha olasiz.")
        serializer.save()

# -------------------- Register --------------------
class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({'message': 'User registered successfully'}, status=201)
# -------------------- Custom User Serializer --------------------