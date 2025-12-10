# authentication/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from django.contrib.auth import authenticate, get_user_model
from django.utils.http import urlsafe_base64_decode
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from .utils import account_activation_token, send_activation_email
from django.utils.http import urlsafe_base64_decode
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from .utils import *
from django.utils.encoding import force_str
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()

# REGISTER VIEW --------------------------------------------------------------
class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_activation_email(request, user)
            return Response(
                {"message": "আপনার রেজিস্ট্রেশন সফল হয়েছে 🎉, দয়া করে ইমেলটি ভেরিফাই করুন।"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# EMAIL VERIFY VIEW
class VerifyEmailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        uid = request.GET.get("uid")
        token = request.GET.get("token")

        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except:
            return Response({"detail": "Invalid UID"}, status=400)

        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.is_email_verified = True
            user.save()
            return Response({"message": "Email Verification Successful, Please Login here."}, status=200)
        else:
            return Response({"detail": "Token invalid or expired"}, status=400)


# LOGIN VIEW -------------------------------------------------------------
class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        device_name_input = request.data.get("device")  


        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response({"detail": "Invalid Creadential"}, status=401)

        if not user.is_active or not getattr(user, "is_email_verified", True):
            return Response({"detail": "Email not verified or user inactive"}, status=status.HTTP_403_FORBIDDEN)
        
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        refresh_token = str(refresh)

        ip = get_client_ip(request)
        ua = request.META.get("HTTP_USER_AGENT", "")
        device_name = device_name_input or get_device_name_from_ua(ua)
        LoginIPHistory.objects.create(user=user, ip_address=ip, user_agent=ua)

        device_qs = LoginDevice.objects.filter(user=user, user_agent=ua, ip_address=ip)
        if device_qs.exists():
            device = device_qs.first()
            device.last_used = timezone.now()
            device.refresh_token = refresh_token  
            device.device_name = device_name
            device.save(update_fields=["last_used", "refresh_token", "device_name"])
        else:
            device = LoginDevice.objects.create(
                user=user,
                device_name=device_name,
                ip_address=ip,
                user_agent=ua,
                refresh_token=refresh_token
            )

        try:
            # Update login metadata
            user.last_login = timezone.now()
            user.last_ip = request.META.get('REMOTE_ADDR')
            user.last_login_device = request.META.get('HTTP_USER_AGENT', '')[:255]
            user.login_count = user.login_count + 1
            user.save(update_fields=["last_login_device", "last_ip", "login_count", "last_login"])
       
        except Exception:
            pass

        return Response({
            "success": True,
            "message": "Your are Successfully Login.",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })
    

# List User Device ------------------------------------------------------
class DeviceListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoginDeviceSerializer

    def get_queryset(self):
        return LoginDevice.objects.filter(user=self.request.user).order_by("-last_used")



# Logout from specific device (blacklist its refresh token)
class DeviceLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, device_id):
        user = request.user
        try:
            device = LoginDevice.objects.get(id=device_id, user=user)
        except LoginDevice.DoesNotExist:
            return Response({"detail": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

        if not device.refresh_token:
            return Response({"detail": "No refresh token stored for this device"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            RefreshToken(device.refresh_token).blacklist()
        except Exception:
    
            pass

        device.refresh_token = None
        device.save(update_fields=["refresh_token"])

        try:
            user.last_logout = timezone.now()
            user.save(update_fields=["last_logout"])
        except Exception:
            pass

        return Response({"message": "Logged out from device"}, status=status.HTTP_200_OK)




# -------------------------
# Block / Unblock a device
# -------------------------
class DeviceBlockAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, device_id):
        # body: {"action": "block"} or {"action": "unblock"}
        action = request.data.get("action")
        if action not in ("block", "unblock"):
            return Response({"detail": "action must be 'block' or 'unblock'."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            device = LoginDevice.objects.get(id=device_id, user=request.user)
        except LoginDevice.DoesNotExist:
            return Response({"detail": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

        device.is_blocked = (action == "block")
        device.save(update_fields=["is_blocked"])
        return Response({"message": f"Device {action}ed"}, status=status.HTTP_200_OK)


# -------------------------
# IP history list
# -------------------------
class IPHistoryListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoginIPHistorySerializer

    def get_queryset(self):
        return LoginIPHistory.objects.filter(user=self.request.user).order_by("-timestamp")


# Logout ---------------------------------------------------

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # if using SimpleJWT Blacklist app
        except Exception:
            return Response({"detail": "Invalid token"}, status=400)

        user = request.user
        user.last_logout = timezone.now()
        user.save(update_fields=["last_logout"])

        return Response({"success": True, "message": "Logout Successful"}, status=200)
    


# Profile ----------------------------------------------------
class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response({"Profile": serializer.data}, status=200)

    def put(self, request):
        serializer = ProfileSerializer(
            request.user,
            data=request.data,
            partial=False,
            context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated", "profile": serializer.data}, status=200)

        return Response(serializer.errors, status=400)

    def patch(self, request):
        serializer = ProfileSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated", "profile": serializer.data}, status=200)

        return Response(serializer.errors, status=400)
    


# Password Reset ---------------------------------------------------------
# Step 1 → Request Password Reset
class PasswordResetRequestAPIView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            send_password_reset_email(request, user)
            return Response({"message": "Password reset email sent."})
        except User.DoesNotExist:
            return Response({"error": "No user with this email."}, status=404)

# Step 2 → Confirm Password Reset
class PasswordResetConfirmAPIView(APIView):
    def post(self, request):
        uid = request.query_params.get("uid")
        token = request.query_params.get("token")

        if not uid or not token:
            return Response({"error": "Invalid request"}, status=400)

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid UID"}, status=400)

        if not password_reset_token.check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=400)

        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.validated_data['new_password'])
        user.save(update_fields=['password'])
        return Response({"message": "Password reset successful."})