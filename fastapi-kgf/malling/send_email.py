from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from core.schemas import TaskRead

import smtplib

from core.config import settings


async def send_email(
    recipient: str,
    subject: TaskRead,
) -> None:
    message = MIMEMultipart()
    message["From"] = settings.superuser.email
    message["To"] = recipient
    message["Subject"] = f"Новая задача {subject.title}"

    msg = f"""
    {subject.title}
    {subject.description}
    http://192.168.1.75:8000/tasks/{subject.project_id}
    """

    message.attach(MIMEText(msg, "plain"))

    server = smtplib.SMTP_SSL("smtp.yandex.com")
    server.ehlo(settings.superuser.email)

    server.login(settings.superuser.email, settings.superuser.email_password)
    server.auth_plain()
    server.sendmail(settings.superuser.email, recipient, message.as_string())
    server.quit()
