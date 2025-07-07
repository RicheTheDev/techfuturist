from flask import current_app, render_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime
import smtplib

def send_otp_email(receiver_email, otp_code):
    subject = "Vérification de votre email - TechFuturists"

    html_content = render_template(
        'email/otp_email.html',
        otp_code=otp_code,
        year=datetime.now().year
    )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = current_app.config["MAIL_SENDER"]
    msg["To"] = receiver_email

    mime_text = MIMEText(html_content, "html", _charset="utf-8")
    msg.attach(mime_text)

    with smtplib.SMTP(current_app.config["MAIL_SERVER"], current_app.config["MAIL_PORT"]) as server:
        server.starttls()
        server.login(current_app.config["MAIL_USERNAME"], current_app.config["MAIL_PASSWORD"])
        server.sendmail(current_app.config["MAIL_SENDER"], receiver_email, msg.as_bytes())

