from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404

from .models import CustomUser
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer
)
from rest_framework import serializers


# Đăng ký tài khoản
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# Đăng nhập → trả về access + refresh token
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Lấy danh sách tất cả người dùng
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# Xem chi tiết 1 người dùng
class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# Xoá người dùng (chỉ admin được phép)
class UserDeleteView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


# Đổi mật khẩu
class ChangePasswordSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    new_password = serializers.CharField(write_only=True)


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data['user_id']
        new_password = serializer.validated_data['new_password']

        user = get_object_or_404(CustomUser, pk=user_id)

        # Admin đổi được bất kỳ ai, member chỉ đổi của chính mình
        if request.user.is_superuser or request.user.id == user.id:
            user.password = make_password(new_password)
            user.save()
            return Response({"detail": "Password changed successfully"})
        else:
            return Response(
                {"detail": "You do not have permission to change this password."},
                status=status.HTTP_403_FORBIDDEN
            )


# Cập nhật thông tin người dùng (chính mình hoặc admin sửa người khác)
class UpdateUserView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Member chỉ được sửa bản thân
        if not self.request.user.is_superuser and self.request.user.id != self.get_object().id:
            raise PermissionDenied("You cannot edit this user.")
        serializer.save()
