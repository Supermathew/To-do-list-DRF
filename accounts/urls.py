from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterAPIView, 
    LoginAPIView,
)
from django.urls import path

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
