import os
import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

MASTER_FOLDER = "12mvSBr6Z-tAUQgwIO2LBZegP20eGAYh9"

def get_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)

def ensure_folder(drive, parent_id, name):
    query = f"'{parent_id}' in parents and trashed=false and mimeType='application/vnd.google-apps.folder' and title='{name}'"
    file_list = drive.ListFile({'q': query}).GetList()
    if file_list:
        return file_list[0]['id']

    folder = drive.CreateFile({
        'title': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [{'id': parent_id}]
    })
    folder.Upload()
    return folder['id']

def save_gumroad_product(title, html_content):
    drive = get_drive()

    today = datetime.datetime.now()
    month_name = today.strftime("%B %Y")  # Example: December 2025

    # level-1 year folder
    month_folder = ensure_folder(drive, MASTER_FOLDER, month_name)

    # stream-specific folder
    stream_folder = ensure_folder(drive, month_folder, "gumroad")

    filename = f"{title}.html"
    file_path = f"/tmp/{filename}"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    gfile = drive.CreateFile({
        'title': filename,
        'parents': [{'id': stream_folder}]
    })

    gfile.SetContentFile(file_path)
    gfile.Upload()

    return gfile['id']
