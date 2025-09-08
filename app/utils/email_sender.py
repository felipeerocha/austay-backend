import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from app.config import settings

def send_email(to_email: str, subject: str, body: str):
    """
    Envia um e-mail usando as configurações do ambiente.
    """
    if not all([settings.EMAIL_HOST, settings.EMAIL_USER, settings.EMAIL_PASS]):
        print("⚠️  AVISO: Credenciais de e-mail não configuradas. O e-mail não será enviado.")
        return

    try:
        msg = MIMEMultipart()
        msg["From"] = formataddr(("Suporte Austay", settings.EMAIL_USER or ""))
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_USER, settings.EMAIL_PASS)
            server.sendmail(settings.EMAIL_USER, to_email, msg.as_string())

        print(f"✅ Email enviado com sucesso para {to_email}")

    except smtplib.SMTPAuthenticationError:
        print("❌ Erro de autenticação. Verifique seu EMAIL_USER e EMAIL_PASS.")
    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado ao enviar o email: {e}")

