# api/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserLoginAPIView

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]