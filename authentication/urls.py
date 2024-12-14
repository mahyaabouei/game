from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import OtpViewSet, LoginViewSet, OtpSejamViewSet, VerifyOtpSejamViewSet, VerifyTokenView



urlpatterns = [
    path('otp/', OtpViewSet.as_view(), name='otp'),
    path('login/', LoginViewSet.as_view(), name='login'),
    path('otp-sejam/', OtpSejamViewSet.as_view(), name='otp-sejam'),
    path('verify-otp-sejam/', VerifyOtpSejamViewSet.as_view(), name='verify-otp-sejam'),
    path('verify-token/', VerifyTokenView.as_view(), name='verify-token'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
