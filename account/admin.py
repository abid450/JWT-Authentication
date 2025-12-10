from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone_number', 'last_ip', 'last_login_device', 'last_login', 'last_logout', 'is_active']


@admin.register(LoginIPHistory)
class LoginIpHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'ip_address', 'user_agent', 'timestamp']



@admin.register(LoginDevice)
class LoginDeviceAdmin(admin.ModelAdmin):
    list_display = [ 'id', 'user', 'device_name', 'ip_address', 'user_agent', 'last_used', 'is_blocked', 'created_at']

   

