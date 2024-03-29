from io import BytesIO
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import requests


class GDrivePhotoMngr:
    def __init__(self, credentials_path, input_url, output_url):
        self.credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.drive_service = build('drive', 'v3', credentials=self.credentials)
        self.input_url = input_url
        self.output_url = output_url

    def get_folder_id_from_url(self, url):
        folder_id = url.split('/')[-1]
        return folder_id

    def list_files_in_folder(self):
        folder_id = self.get_folder_id_from_url(self.input_url)
        results = self.drive_service.files().list(
            q=f"'{folder_id}' in parents",
            fields="files(id, name)"
        ).execute()
        return results.get('files', [])

    def download_image_as_bytes(self, file_id):
        file_response = self.drive_service.files().get_media(fileId=file_id).execute()
        return file_response

    def get_images_as_bytes(self):
        # List files in the specified folder
        files = self.list_files_in_folder()

        images_bytes_list = []
        # Download each image file and convert it into bytes
        for file in files:
            file_id = file['id']
            image_bytes = self.download_image_as_bytes(file_id)
            images_bytes_list.append(image_bytes)

        return images_bytes_list

    def upload_images_to_folder(self, images_bytes_list):
        folder_id = self.get_folder_id_from_url(self.output_url)
        for idx, image_bytes in enumerate(images_bytes_list):
            file_metadata = {'name': f'image_{idx + 1}.jpg', 'parents': [folder_id]}
            media = MediaIoBaseUpload(BytesIO(image_bytes), mimetype='image/jpeg', resumable=True)
            file = self.drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f'Image {idx + 1} uploaded with ID: {file.get("id")}')


