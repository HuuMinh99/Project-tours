from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'full_name', 'phone', 'address']
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            role='member'  # Mặc định là member
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        from django.contrib.auth import authenticate
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class ChangePasswordSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate(self, data):
        try:
            user = User.objects.get(id=data['user_id'])
            data['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")
        return data

    def save(self, **kwargs):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
