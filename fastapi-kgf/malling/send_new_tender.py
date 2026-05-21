import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from core.config import settings
from core.schemas import TenderCreate


def get_html_content(subject: list[TenderCreate]) -> str:
    start_html = f"""
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
                <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: bold;">📊 Новые тендеры</h1>
            </td>
        </tr>

        <!-- Content -->
        <tr>
            <td style="padding: 30px 40px;">
                
                <!-- Общая информация -->
                <p style="color: #666666; font-size: 14px; margin: 0 0 5px 0; text-transform: uppercase; letter-spacing: 1px;">📋 Количество тендеров</p>
                <p style="color: #333333; font-size: 28px; font-weight: bold; margin: 0 0 25px 0; border-bottom: 2px solid #667eea; padding-bottom: 15px;">
                    {len(subject)}
                </p>

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
"""
    tenders_html = ""

    for tender in subject[:3]:
        tenders_html += f"""
        <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 20px; background-color: #f8f9fa; border-radius: 8px; border: 1px solid #e9ecef;">
                    
                    <tr>
                        <td style="padding: 15px 20px; background-color: #667eea; border-radius: 8px 8px 0 0;">
                            <h3 style="color: #ffffff; margin: 0; font-size: 16px;">
                                {tender.name}
                            </h3>
                        </td>
                    </tr>

                    <tr>
                        <td style="padding: 20px;">
                            <table cellpadding="0" cellspacing="0" border="0" width="100%">

                                <tr>
                                    <td style="padding: 6px 0; border-bottom: 1px solid #e9ecef;">
                                        <span style="color: #999999; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Заказчик</span>
                                    </td>
                                    <td style="padding: 6px 0; border-bottom: 1px solid #e9ecef; text-align: right;">
                                        <span style="color: #333333; font-size: 14px;">{tender.organizer}</span>
                                    </td>
                                </tr>

                                <tr>
                                    <td style="padding: 6px 0; border-bottom: 1px solid #e9ecef;">
                                        <span style="color: #999999; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Начальная цена</span>
                                    </td>
                                    <td style="padding: 6px 0; border-bottom: 1px solid #e9ecef; text-align: right;">
                                        <span style="color: #667eea; font-size: 16px; font-weight: bold;">{tender.price}</span>
                                    </td>
                                </tr>

                                <tr>
                                    <td style="padding: 6px 0;">
                                        <span style="color: #999999; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Дата окончания</span>
                                    </td>
                                    <td style="padding: 6px 0; text-align: right;">
                                        <span style="color: #dc3545; font-size: 14px; font-weight: bold;">{tender.end_date.date()}</span>
                                    </td>
                                </tr>

                            </table>

                            <div style="text-align: center; margin-top: 15px;">
                                <a href="{tender.url}" 
                                   style="display: inline-block; padding: 8px 25px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; text-decoration: none; border-radius: 20px; font-size: 13px; font-weight: bold;">
                                    🔗 Перейти к тендеру
                                </a>
                            </div>

                        </td>
                    </tr>

                </table>
                """
    end_html = """

                <!-- Кнопка ко всем тендерам -->
                <div style="text-align: center; margin: 25px 0;">
                    <a href="http://192.168.1.75:8000/tenders" 
                       style="display: inline-block; padding: 12px 35px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; text-decoration: none; border-radius: 25px; font-size: 16px; font-weight: bold; box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);">
                        📋 Смотреть все тендеры
                    </a>
                </div>

            </td>
        </tr>

        <!-- Footer -->
        <tr>
            <td style="background-color: #f8f9fa; padding: 20px 40px; text-align: center; border-top: 1px solid #e9ecef;">
                <p style="color: #999999; font-size: 12px; margin: 0 0 10px 0;">
                    Это автоматическое уведомление от системы мониторинга тендеров
                </p>
            </td>
        </tr>
        
    </table>
</body>
</html>"""

    return start_html + tenders_html + end_html


async def send_new_tenders(
    recipient: str,
    subject: list[TenderCreate],
) -> None:
    message = MIMEMultipart()
    message["From"] = settings.superuser.email
    message["To"] = recipient
    message["Subject"] = "Новые тендера"

    msg = get_html_content(subject)

    message.attach(MIMEText(msg, "html"))

    server = smtplib.SMTP_SSL("smtp.yandex.com")
    server.ehlo(settings.superuser.email)

    server.login(
        settings.superuser.email,
        settings.email_password,
    )
    server.auth_plain()
    server.sendmail(
        settings.superuser.email,
        recipient,
        message.as_string(),
    )
    server.quit()
