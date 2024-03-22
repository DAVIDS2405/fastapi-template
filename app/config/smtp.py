from dotenv import load_dotenv
import os
from fastapi.templating import Jinja2Templates
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

load_dotenv()


templates = Jinja2Templates(directory="app/templates")


def send_email(name, year, token):

    smtp_server = os.getenv("EMAIL_HOST")
    smtp_port = int(os.getenv("EMAIL_PORT"))
    smtp_username = os.getenv("EMAIL_HOST_USER")
    smtp_password = os.getenv("EMAIL_HOST_PASSWORD")

    msg = MIMEMultipart()
    msg['From'] = "Acme <onboarding@resend.dev>"
    msg['To'] = "delivered@resend.dev"
    msg['Subject'] = "¡Bienvenido completa tu registro!"

    template = templates.get_template("email-send.html")

    html_content = template.render(name=name, year=year, token=token)

    msg.attach(MIMEText(html_content, 'html'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)

        return True
    except Exception as e:

        print(f"Error al enviar el correo electrónico: {e}")
        return False


def send_email_reset_password(name, year, id):

    smtp_server = os.getenv("EMAIL_HOST")
    smtp_port = int(os.getenv("EMAIL_PORT"))
    smtp_username = os.getenv("EMAIL_HOST_USER")
    smtp_password = os.getenv("EMAIL_HOST_PASSWORD")

    msg = MIMEMultipart()
    msg['From'] = "Acme <onboarding@resend.dev>"
    msg['To'] = "delivered@resend.dev"
    msg['Subject'] = "Recupera tu contraseña"

    template = templates.get_template("recover-password.html")

    html_content = template.render(name=name, year=year, id=id)

    msg.attach(MIMEText(html_content, 'html'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)

        return True
    except Exception as e:

        print(f"Error al enviar el correo electrónico: {e}")
        return False
