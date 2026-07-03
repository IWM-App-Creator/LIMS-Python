from app.properties.globalproperties import globalps
from app.properties.notificationproperties import notifyps
import smtplib
from email.message import EmailMessage

def sendEmail():
    print("sendEmail --> ", notifyps.to_email, notifyps.subject, notifyps.body, notifyps.html, notifyps.cc, notifyps.bcc)
    print("sendEmail --> ", globalps.MAIL_FROM_ADDRESS, ":", globalps.MAIL_HOST, ":", globalps.MAIL_PORT, ":", globalps.MAIL_USERNAME, globalps.MAIL_PASSWORD)
    msg = EmailMessage()

    msg["Subject"] = notifyps.subject
    msg["From"] = globalps.MAIL_FROM_ADDRESS
    msg["To"] = ", ".join(notifyps.to_email) if isinstance(notifyps.to_email, list) else notifyps.to_email

    if notifyps.cc:
        msg["Cc"] = ", ".join(notifyps.cc) if isinstance(notifyps.cc, list) else notifyps.cc

    if notifyps.html:
        msg.add_alternative(notifyps.body, subtype="html")
    else:
        msg.set_content(notifyps.body)

    # if attachments:
    #     for file in attachments:
    #         path = Path(file)
    #         with open(path, "rb") as f:
    #             msg.add_attachment(
    #                 f.read(),
    #                 maintype="application",
    #                 subtype="octet-stream",
    #                 filename=path.name
    #             )

    # Combine all recipients for SMTP
    recipients = []

    if isinstance(notifyps.to_email, list):
        recipients.extend(notifyps.to_email)
    else:
        recipients.append(notifyps.to_email)

    if notifyps.cc:
        if isinstance(notifyps.cc, list):
            recipients.extend(notifyps.cc)
        else:
            recipients.append(notifyps.cc)

    if notifyps.bcc:
        if isinstance(notifyps.bcc, list):
            recipients.extend(notifyps.bcc)
        else:
            recipients.append(notifyps.bcc)

    with smtplib.SMTP(globalps.MAIL_HOST, globalps.MAIL_PORT) as smtp:
        smtp.starttls()
        smtp.login(globalps.MAIL_USERNAME, globalps.MAIL_PASSWORD)
        smtp.send_message(msg, to_addrs=recipients)

    print("Email sent successfully!!")