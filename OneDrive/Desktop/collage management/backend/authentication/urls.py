from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('verify-token/', views.verify_token, name='verify-token'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token-refresh'),
    path('setup/', views.complete_setup, name='complete-setup'),
]
