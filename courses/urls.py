# courses/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, CategoryViewSet, VideoContentViewSet, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'videos', VideoContentViewSet, basename='video')

urlpatterns = [
    path('api/', include(router.urls)),
    
    # Auth
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='login'),  # JWT login
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
