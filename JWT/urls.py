"""
URL configuration for JWT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from account.views import *
from django.views.generic import TemplateView
from college.views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('month_r', AttendanceMonthlyReportView, basename='monthlyreport')
router.register('students', StudentView, basename='students')
router.register('marks', MarkViewSet, basename='marks')
router.register('attendance-create', AttendanceCreateViewSet, basename='attendance-create')
router.register('attendance', AttendanceViewSet, basename='attendance')


urlpatterns = router.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminpanel', TemplateView.as_view(template_name='attendenceSummary.html'), name='summary'),
    path('attendencepanel', TemplateView.as_view(template_name='attendence.html'), name='attendence'),


    path('api/', include(router.urls)),
    path('signup', RegisterAPIView.as_view(), name='signup'),
    path('login_info', TemplateView.as_view(template_name="login.html")),
    path('signup_info', TemplateView.as_view(template_name="signup.html")),
    path('login', LoginAPIView.as_view(), name='login'),
    path("devices/", DeviceListAPIView.as_view(), name="device-list"),
    path("devices/<int:device_id>/logout/", DeviceLogoutAPIView.as_view(), name="device-logout"),
    path("devices/<int:device_id>/block/", DeviceBlockAPIView.as_view(), name="device-block"),
    path("ip-history/", IPHistoryListAPIView.as_view(), name="ip-history"),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path("verify-email/", VerifyEmailAPIView.as_view(), name="verify-email"),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path("reset-password/", PasswordResetRequestAPIView.as_view(), name="reset-password"),
    path("reset-password-confirm/", PasswordResetConfirmAPIView.as_view(), name="reset-password-confirm"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

