from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.user.views import UserRegisterCreateAPIView, UserGetMeApiView

urlpatterns = [
    path('admin/register', UserRegisterCreateAPIView.as_view(), name='user-register'),
    path('user/login', TokenObtainPairView.as_view(), name='user-login'),
    path('user/get-me', UserGetMeApiView.as_view(), name='user-get-me'),
]
