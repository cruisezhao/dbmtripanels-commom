from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings

def send_reply_email(files,recipients, subject, body, fail_silently=False, sender=None):
    """send email"""
    if not sender:
        sender = settings.DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(
        subject, body, sender, recipients)

    if files:
        for attachment in files:
            file_to_attach = attachment[1]
            file_to_attach.open()
            msg.attach(filename=attachment[0], content=file_to_attach.read())
            file_to_attach.close()

    return msg.send(fail_silently)