import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from core.config import settings
from core.schemas import TaskRead


def get_html_content(subject: TaskRead) -> str:
    task_url = f'http://192.168.1.75:8000/projects/{subject.project_id}'
    return f"""
 <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; background-color: #f4f4f9; font-family: Arial, sans-serif;">
        <table cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; margin-top: 20px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <!-- Header -->
            <tr>
                <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px 40px; text-align: center;">
                    <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: bold;">📋 Новая задача</h1>
                </td>
            </tr>

            <!-- Content -->
            <tr>
                <td style="padding: 30px 40px;">
                    <!-- Task Title -->
                    <h2 style="color: #333333; font-size: 20px; margin: 0 0 20px 0; border-bottom: 2px solid #667eea; padding-bottom: 10px;">
                        {subject.title}
                    </h2>

                    <!-- Access Warning -->
                    <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 25px; background-color: #fff3cd; border: 1px solid #ffc107; border-radius: 8px;">
                        <tr>
                            <td style="padding: 12px 15px;">
                                <p style="color: #856404; font-size: 13px; margin: 0; line-height: 1.5;">
                                    ⚠️ <strong>Важно!</strong> Доступ к системе возможен только с рабочих компьютеров «Казаньгеофизика»
                                </p>
                            </td>
                        </tr>
                    </table>

                    <!-- Description -->
                    <div style="margin-bottom: 30px;">
                        <p style="color: #666666; font-size: 14px; margin: 0 0 5px 0; text-transform: uppercase; letter-spacing: 1px;">📝 Описание задачи</p>
                        <p style="color: #333333; font-size: 16px; line-height: 1.6; margin: 0; background-color: #f8f9fa; padding: 15px; border-radius: 6px; border-left: 4px solid #667eea;">
                            {subject.description or "Описание отсутствует"}
                        </p>
                    </div>

                    <!-- Button -->
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{task_url}" 
                           style="display: inline-block; padding: 12px 35px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; text-decoration: none; border-radius: 25px; font-size: 16px; font-weight: bold; box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);">
                            🔗 Перейти к задаче
                        </a>
                    </div>

                    <!-- Link -->
                    <div style="text-align: center; margin-top: 20px; padding: 15px; background-color: #f8f9fa; border-radius: 6px;">
                        <p style="color: #666666; font-size: 13px; margin: 0 0 5px 0;">Или скопируйте ссылку:</p>
                        <a href="{task_url}" style="color: #667eea; font-size: 13px; word-break: break-all;">{task_url}</a>
                    </div>
                </td>
            </tr>

            <!-- Footer -->
            <tr>
                <td style="background-color: #f8f9fa; padding: 20px 40px; text-align: center; border-top: 1px solid #e9ecef;">
                    <p style="color: #999999; font-size: 12px; margin: 0 0 10px 0;">
                        Это автоматическое уведомление от системы управления задачами
                    </p>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


async def send_email(
    recipient: str,
    subject: TaskRead,
) -> None:
    message = MIMEMultipart()
    message["From"] = settings.superuser.email
    message["To"] = recipient
    message["Subject"] = f"Новая задача {subject.title}"

    msg = get_html_content(subject)

    message.attach(MIMEText(msg, "html"))

    await aiosmtplib.send(
        message,
        hostname="smtp.yandex.com",
        port=587,
        username=settings.superuser.email,
        password=settings.email_password,
    )