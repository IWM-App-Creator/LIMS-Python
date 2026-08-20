from app.utils.common import globalps, formatDate, getTimeAgoValue
from app.helper.generalfunctions import formatUserDisplayName
from pathlib import Path
import smtplib
from email.message import EmailMessage
from app.dbfunctions.notificationfunctions import getNotificationList, getNotificationData, getNotificationCountViews, insertUpdateNotification
from app.dbfunctions.menufunctions import getActiveMenuDB, insertUpdateMenuCentre
from app.helper.noteshelper import getSmileyNotesMap
from app.helper.generalfunctions import normalizeJson
from app.properties.notesproperties import notesps
from app.properties.menuproperties import menups

def getNotifications(notifyps):
    notificationarr = getNotificationList(notifyps)
    notification_list = []
    note_ids = [getattr(n, "notes_id", 0) for n in notificationarr if n.notes_id]
    notesps.note_ids.set(note_ids)
    smilemap = getSmileyNotesMap(notesps)
    for noti in notificationarr:
        if noti:
            from_user_nm = getattr(noti, "from_user_name", "").replace("**", " ")
            to_user_nm = getattr(noti, "to_user_name", "").replace("**", " ")
            if int(notifyps.is_new.get()) == 1:
                row = {
                    "noti_type": getattr(noti, "noti_type", ""),
                    "to_user_id": getattr(noti, "to_user_id", 0),
                    "title": getattr(noti, "title", ""),
                    "message": getattr(noti, "message", ""),
                    "is_new": 1
                }
            else:
                row = {
                    "notificaitons_id": getattr(noti, "notificaitons_id", 0),
                    "noti_type": getattr(noti, "noti_type", ""),
                    "item_id": getattr(noti, "item_id", 0),
                    "view_id": getattr(noti, "view_id", 0),
                    "view_name": getattr(noti, "view_name", 0),
                    "view_url": getattr(noti, "url", 0),
                    "notes_id": getattr(noti, "notes_id", 0),
                    "parent_id": getattr(noti, "parent_id", 0),
                    "item_id": getattr(noti, "item_id", 0),
                    "title": getattr(noti, "title", ""),
                    "message": getattr(noti, "message", ""),
                    "msg_data": getattr(noti, "msg_data", ""),
                    "is_read": getattr(noti, "is_read", 0),
                    "read_date": formatDate(getattr(noti, "read_date", None), "%Y-%m-%d %H:%M:%S"),
                    "is_new": getattr(noti, "is_new", 0),
                    "is_archive": getattr(noti, "is_archive", 0),
                    "is_outbox": int(notifyps.is_outbox.get() or 0),
                    "smiley_list": smilemap.get(getattr(noti, "notes_id", 0), []),
                    "to_user": to_user_nm,
                    "to_user_init_nm": formatUserDisplayName(getattr(noti, "to_user_name", "").split("**")[0], getattr(noti, "to_user_name", "").split("**")[1], "INITIAL"),
                    "created_by": from_user_nm,
                    "created_by_init_nm": formatUserDisplayName(getattr(noti, "from_user_name", "").split("**")[0], getattr(noti, "from_user_name", "").split("**")[1], "INITIAL"),
                    "created_date": formatDate(getattr(noti, "created_date", None), "%Y-%m-%d %H:%M:%S"),
                    "time_ago": getTimeAgoValue(getattr(noti, "created_date", None)),
                }
            notification_list.append(row)
    return notification_list

def getNotificationCount(notifyps):
    noti_vw_data = getNotificationCountViews(notifyps)
    noti_views = []
    for noti in noti_vw_data:
        row = {
            "view_id": getattr(noti, "view_id", 0),
            "view_name": getattr(noti, "view_name", ""),
            "cnt": getattr(noti, "cnt", 0),
        }
        noti_views.append(row)
    return noti_views

def acceptNotificationData(notifyps):
    flag = notifyps.flag.get().upper()
    if flag == "REMOVE":
        notifyps.upd_vals.set({"is_delete": 1})
    elif flag == "SAVEMENU":
        noti_data = getNotificationData(notifyps)
        if noti_data and getattr(noti_data, "msg_data", "") not in (None, "", {}):
            msg_data = normalizeJson(getattr(noti_data, "msg_data", {}), {})
            menups.m_centre_id.set(msg_data.get("m_center_id", 0))
            menu_data = getActiveMenuDB(menups)
            if menu_data:
                menups.m_centre_id.set(None)
                menups.upd_vals.set({
                    "centre_name": getattr(menu_data, "centre_name", ""),
                    "ref_m_c_id": msg_data.get("m_center_id", 0),
                    "menu_json": getattr(menu_data, "menu_json", []),
                    "is_public": 0,
                    "is_active": 0,
                })
                insertUpdateMenuCentre(menups)
    elif flag == "SAVEFILTER":
        print("filter save")
    notifyps.upd_vals.set({"msg_data": ""})
    insertUpdateNotification(notifyps)

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