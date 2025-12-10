# authentication/utils.py

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site

class ActivationTokenGenerator(PasswordResetTokenGenerator):
    pass

# Token generator instance
account_activation_token = ActivationTokenGenerator()

# Send activation email
def send_activation_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    domain = get_current_site(request).domain

    relative_link = "/verify-email/"
    activate_url = f"{request.scheme}://{domain}{relative_link}?uid={uid}&token={token}"

    subject = "আপনার অ্যাকাউন্ট Verify করুন"
    message = f"""
    হ্যালো {user.username},

    নিচের লিংকে ক্লিক করে আপনার অ্যাকাউন্টটি verify করুন:

    {activate_url}

    ধন্যবাদ!
    """

    send_mail(
        subject,
        message,
        None,
        [user.email],
        fail_silently=False,
    )

    return activate_url


# Password Reset
password_reset_token = PasswordResetTokenGenerator()

def send_password_reset_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = password_reset_token.make_token(user)
    domain = get_current_site(request).domain

    reset_url = f"{request.scheme}://{domain}/reset-password-confirm/?uid={uid}&token={token}"

    subject = "Reset your password"
    message = f"""
    Hello {user.username},

    Click the link below to reset your password:

    {reset_url}

    If you did not request a password reset, ignore this email.
    """
    send_mail(subject, message, None, [user.email], fail_silently=False)
    return reset_url




from django.utils import timezone

def get_client_ip(request):
    """Simple helper to get real client IP (considers X-Forwarded-For)."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # X-Forwarded-For: client, proxy1, proxy2
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip or ""

def get_device_name_from_ua(ua_string: str) -> str:
    """
    Very simple UA -> device string. For production, use `user-agents` or `ua-parser`.
    """
    if not ua_string:
        return "Unknown Device"
    ua = ua_string.lower()
    if "mobile" in ua or "android" in ua or "iphone" in ua:
        return "Mobile - " + (ua_string.split(")")[0] if ")" in ua_string else ua_string)[:100]
    if "windows" in ua:
        return "Windows - " + (ua_string.split(")")[0] if ")" in ua_string else ua_string)[:100]
    if "macintosh" in ua or "mac os" in ua:
        return "Mac - " + (ua_string.split(")")[0] if ")" in ua_string else ua_string)[:100]
    return ua_string[:150]
