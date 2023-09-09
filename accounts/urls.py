from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (CustomTokenObtainPairView,
                    UserRegisterAPI,
                    UserAccountVerificationAPI,
                    UserReVerificationAPI,
                    ForgetPasswordAPI,
                    PasswordResetAPI,
                    UserProfileAPI
                    )

urlpatterns = [
    path('register/', UserRegisterAPI.as_view()),
    path('token/', CustomTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('verify/', UserAccountVerificationAPI.as_view()),
    path('re-verify/', UserReVerificationAPI.as_view()),
    path('forget-password/', ForgetPasswordAPI.as_view()),
    path('password-reset/', PasswordResetAPI.as_view()),
    path('profile/<str:username>/', UserProfileAPI.as_view()),
]
