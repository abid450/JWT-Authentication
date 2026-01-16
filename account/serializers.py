# account/serializers.py
from rest_framework import serializers
from .models import User
import re
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import *


User = get_user_model()

# Register -------------------------------------------------
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "phone_number",   "first_name", "last_name",  "last_login_device", "last_ip", "last_login", "last_logout", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, email):
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("Email already exists")
        return email

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    

    def validate_phone_number(self, value):
        phone = value.strip()
        pattern = r'^(013|014|015|016|017|018|019)\d{8}$'
        if not re.match(pattern, phone):
            raise serializers.ValidationError("Enter a valid Phone number.")
        
        elif User.objects.filter(phone_number=phone).exists():
            raise serializers.ValidationError('Phone Number is already exist.')
        return phone
    
    
    def validate_password(self, password):
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$', password):
            raise serializers.ValidationError("Password does not meet security requirements.")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# Profile ------------------------------------------------------
from rest_framework import serializers
from .models import User

class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "phone_number",
            "last_ip",
            "last_login_device",
            "last_login",
            "last_logout",
            "login_count",
            "is_email_verified",
        ]

        read_only_fields = [
            "last_ip",
            "last_login_device",
            "last_login",
            "last_logout",
            "login_count",
            "is_email_verified",
        ]

    # email already exists check
    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    # username already exists check
    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("Username already in use.")
        return value



# password Reset ----------------------------------------------------------------
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords did not match.")
        return attrs
    


# Login Device ----------------------------------------------------------------
class LoginDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginDevice
        fields = [
            "id", "device_name", "ip_address", "user_agent",
            "last_used", "is_blocked", "created_at"
        ]
        read_only_fields = ["id", "ip_address", "user_agent", "last_used", "created_at"]



#ip history ----------------------------------------------------------------
class LoginIPHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginIPHistory
        fields = ["id", "ip_address", "user_agent", "timestamp"]
        read_only_fields = fields