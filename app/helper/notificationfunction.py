from app.properties.globalproperties import globalps
from pathlib import Path
import smtplib
from email.message import EmailMessage

def sendEmail(notifyps):
    msg = EmailMessage()
    msg["Subject"] = notifyps.subject.get()
    from_email = globalps.MAIL_FROM_ADDRESS
    from_name = globalps.MAIL_FROM_NAME
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = ", " . join(notifyps.to_email.get()) if isinstance(notifyps.to_email.get(), list) else notifyps.to_email.get()

    if notifyps.cc.get():
        msg["Cc"] = ", ".join(notifyps.cc.get()) if isinstance(notifyps.cc.get(), list) else notifyps.cc.get()

    if notifyps.html.get():
        msg.add_alternative(notifyps.html.get(), subtype="html")
    else:
        msg.set_content(notifyps.body.get())

    if notifyps.attachments.get():
        for file in notifyps.attachments.get():
            path = Path(file)
            with open(path, "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype="application",
                    subtype="octet-stream",
                    filename=path.name
                )

    # Combine all recipients for SMTP
    recipients = []
    if isinstance(notifyps.to_email.get(), list):
        recipients.extend(notifyps.to_email.get())
    else:
        recipients.append(notifyps.to_email.get())

    if notifyps.cc.get():
        if isinstance(notifyps.cc.get(), list):
            recipients.extend(notifyps.cc.get())
        else:
            recipients.append(notifyps.cc.get())

    if notifyps.bcc.get():
        if isinstance(notifyps.bcc.get(), list):
            recipients.extend(notifyps.bcc.get())
        else:
            recipients.append(notifyps.bcc.get())

    with smtplib.SMTP(globalps.MAIL_HOST, globalps.MAIL_PORT) as smtp:
        smtp.starttls()
        smtp.login(globalps.MAIL_USERNAME, globalps.MAIL_PASSWORD)
        smtp.send_message(msg, to_addrs=recipients)