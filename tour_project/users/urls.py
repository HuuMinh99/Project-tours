from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView, LoginView,
    UserListView, UserDetailView, UserDeleteView,
    ChangePasswordView, UpdateUserView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('<int:pk>/update/', UpdateUserView.as_view(), name='user-update'),
]
