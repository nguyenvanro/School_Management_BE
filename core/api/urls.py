# api/urls.py
from django.urls import path
from .views import UserLoginAPIView
from rest_framework.routers import DefaultRouter
from .views import (
    UserLoginAPIView,
    TeacherProfileViewSet, ParentProfileViewSet, StudentProfileViewSet,
    GradeViewSet, SubjectViewSet, LessonViewSet, ClassViewSet
)
from rest_framework_simplejwt.views import TokenRefreshView


router = DefaultRouter()
router.register(r'teachers', TeacherProfileViewSet)
router.register(r'parents', ParentProfileViewSet)
router.register(r'students', StudentProfileViewSet)
router.register(r'grades', GradeViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'lessons', LessonViewSet)


urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls