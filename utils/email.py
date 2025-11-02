from django.core.mail import get_connection
from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings


def send_email_with_backend(
    subject,
    message,
    recipient_list,
    html_message=None,
    backend_key=None,
    fail_silently=False
):
    """
    Send email using a specific backend from EMAIL_BACKENDS dictionary.
    
    Args:
        subject: Email subject
        message: Plain text message
        recipient_list: List of recipient email addresses
        html_message: Optional HTML message
        backend_key: Key from EMAIL_BACKENDS dictionary (defaults to DEFAULT_EMAIL_BACKEND_KEY)
        fail_silently: If True, exceptions will be silently ignored
    
    Returns:
        Number of emails sent (0 if failed)
    """
    if backend_key is None:
        backend_key = settings.DEFAULT_EMAIL_BACKEND_KEY
    
    if backend_key not in settings.EMAIL_BACKENDS:
        raise ValueError(f"Email backend key '{backend_key}' not found in EMAIL_BACKENDS")
    
    email_config = settings.EMAIL_BACKENDS[backend_key]
    
    # Configure connection
    connection = get_connection(
        backend=email_config["backend"],
        host=email_config["host"],
        port=email_config["port"],
        username=email_config["email_user"],
        password=email_config["email_password"],
        use_tls=email_config["use_tls"],
        use_ssl=email_config["use_ssl"],
        fail_silently=fail_silently,
    )
    
    # Create email message
    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=email_config["default_from_email"],
        to=recipient_list,
        connection=connection,
    )
    
    # Attach HTML message if provided
    if html_message:
        email.attach_alternative(html_message, "text/html")
    
    # Send email
    return email.send()

