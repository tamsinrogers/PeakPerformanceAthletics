from __future__ import print_function

import json
# import os.path
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import io

import google.auth
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SCOPES = ['https://www.googleapis.com/auth/drive']

def build_credentials_json() -> dict:
    # call Credentials.from_authorized_user_info on the result of this function
    json_dict = {
        "installed": {
            "client_id":os.environ["GOOGLE_CREDENTIALS_CLIENT_ID"],
            "project_id":"peakperformanceathletics",
            "auth_uri":"https://accounts.google.com/o/oauth2/auth",
            "token_uri":"https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
            "client_secret":os.environ["GOOGLE_CREDENTIALS_CLIENT_SECRET"],
            "redirect_uris":["http://localhost"]
        }
    }

    return json_dict


def build_token_json() -> dict:
    # call Credentials.from_authorized_user_info on the result of this function
    json_dict = {
        "token":os.environ["GOOGLE_TOKEN"],
        "refresh_token":os.environ["GOOGLE_REFRESH_TOKEN"],
        "token_uri":"https://oauth2.googleapis.com/token",
        "client_id":os.environ["GOOGLE_CREDENTIALS_CLIENT_ID"],
        "client_secret":os.environ["GOOGLE_CREDENTIALS_CLIENT_SECRET"],
        "scopes": ["https://www.googleapis.com/auth/drive"],
        "expiry": "2022-12-06T22:35:14.757399Z"
    }

    return json_dict


def search_csvs():
    """Search file in drive location

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    token_dict = build_token_json()
    creds = Credentials.from_authorized_user_info(token_dict, SCOPES)

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        files = []
        page_token = None
        while True:
            # pylint: disable=maybe-no-member
            response = service.files().list(q="name contains 'csv' and name contains 'ppa'",
                                            spaces='drive',
                                            fields='nextPageToken, '
                                                   'files(id, name)',
                                            pageToken=page_token).execute()
            # for file in response.get('files', []):
            #     # Process change
            #     print(F'Found file: {file.get("name")}, {file.get("id")}')
            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        # filter files to only include csvs
        files = [file for file in files if file.get("name").endswith(".csv")]


    except HttpError as error:
        print(F'An error occurred: {error}')
        files = None

    return files


def download_csv(real_file_id):
    """Downloads a file
    Args:
        real_file_id: ID of the file to download
    Returns : IO object with location.

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    # creds, _ = google.auth.default()
    token = build_token_json()
    creds = Credentials.from_authorized_user_info(token, SCOPES)

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        file_id = real_file_id

        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(F'Download {int(status.progress() * 100)}.')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.getvalue()


def write_csv(file_io, file_name:str, path="."):
    """Writes a CSV to the file system."""

    with open(f"{path}/{file_name}", "wb") as the_file:
        the_file.write(file_io)


def download_all_csvs():
    """Downloads all csv files to file system."""
    # get all csvs
    all_csvs = search_csvs()

    for csv in all_csvs:
        downloaded_file = download_csv(csv.get("id"))
        write_csv(downloaded_file, csv.get("name"), path="../csvs")


if __name__ == '__main__':
    # main()
    a = search_csvs()
    print(type(a))
    # print(a)
    print(type(a[0]))
    print(a[0])

    download_all_csvs()

    