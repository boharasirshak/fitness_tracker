from pathlib import Path
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.config import smtp
from app.config import (
    SMTP_USER,
    SMTP_PASS,
    SMTP_FROM_NAME
)


async def init_smtp():
    await smtp.connect()
    await smtp.starttls()
    await smtp.login(SMTP_USER, SMTP_PASS)


def read_email_template(filename: str):
    current_file_path = Path(__file__).resolve()
    project_root = current_file_path.parents[2]  # navigate 2 levels up

    # construct the url using the pathlib `/` operator
    template_path = project_root / 'app' / 'templates' / 'emails' / filename

    with open(template_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


async def send_mail_async(
        to: str,
        subject: str,
        html: str
):
    """Send an outgoing email with the given parameters.

    :param to: A list of recipient email addresses.
    :type to: list

    :param subject: The subject of the email.
    :type subject: str

    :param html: The text of the email.
    :type html: str
    """

    # Prepare Message
    msg = MIMEMultipart()
    msg.preamble = subject
    msg['Subject'] = subject
    msg['From'] = Header(SMTP_FROM_NAME, 'utf-8')
    msg['To'] = to

    msg.attach(MIMEText(html, "html", "utf-8"))

    await smtp.send_message(msg)
    await smtp.quit()
