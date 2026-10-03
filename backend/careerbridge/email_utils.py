from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def send_otp_email(to_email, code, purpose="signup"):
    if purpose == "login":
        subject = "Your CareerBridge AI login code"
        intro = "Use this code to sign in to your CareerBridge AI account."
    elif purpose == "reset":
        subject = "Your CareerBridge AI password reset code"
        intro = "Use this code to reset your CareerBridge AI password."
    else:
        subject = "Your CareerBridge AI verification code"
        intro = "Use this code to verify your CareerBridge AI account."

    text_body = (
        f"{intro}\n\n"
        f"Your 6-digit code is: {code}\n\n"
        "This code expires in 10 minutes.\n\n"
        "If you did not request this code, you can safely ignore this email."
    )

    html_body = f"""
    <!DOCTYPE html><html><body style="font-family:Arial,sans-serif;line-height:1.6;">
    <h2>CareerBridge AI</h2><p>{intro}</p>
    <div style="display:inline-block;padding:14px 22px;background:#0D1220;color:#22D3EE;font-size:28px;font-weight:bold;letter-spacing:8px;border-radius:8px;">{code}</div>
    <p>This code expires in <strong>10 minutes</strong>.</p>
    <p>If you did not request this code, you can safely ignore this email.</p>
    <p>— CareerBridge AI</p></body></html>
    """

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )
    email.attach_alternative(html_body, "text/html")
    email.send(fail_silently=False)
    return "smtp"
