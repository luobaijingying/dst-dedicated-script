from concurrent.futures import ThreadPoolExecutor
import os
import sys
import requests
import mimetypes
from urllib import parse

FILE_SERVER = "https://xxxxxxxxxx"
LOGIN_API_URL = f"{FILE_SERVER}/api/auth/login"
LIST_API_URL = f"{FILE_SERVER}/api/fs/list"
GET_API_URL = f"{FILE_SERVER}/api/fs/get"
PUT_API_URL = f"{FILE_SERVER}/api/fs/put"
USERNAME = "xxxx"
PASSWORD = "xxxxxxx"
DIRECTORY_PATH = "/dstbackup"

def login(username, password):
    login_payload = {
        "username": username,
        "password": password
    }
    response = requests.post(LOGIN_API_URL, json=login_payload)
    if response.status_code == 200:
        data = response.json()
        if data["code"] == 200:
            return data["data"]["token"]
    return None

def upload(token, filepath, filename):
    filefullpath=f"{filepath}/{filename}"
    filesize = os.path.getsize(filefullpath)
    filetype, encoding = mimetypes.guess_type(filefullpath)
    with open(filefullpath, '+rb') as f:
        if filetype == None:
            filetype = "application/octet-stream"
        headers = {
            "Authorization": f"{token}",
            "File-Path": parse.quote(f"{DIRECTORY_PATH}/{filename}"),
            "As-Task": "true",
            "Content-Type": filetype,
            "Content-Length": f"{filesize}"
        }
        print(headers)
        res = requests.put(PUT_API_URL, headers=headers, data=f)
        print(res.text)

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) < 3:
        print('Invalid command. Usage: python dstbackup.py filepath filename')
        exit(1)
    filepath = sys.argv[1]
    filename = sys.argv[2]
    token = login(USERNAME, PASSWORD)
    if token:
        print(f"登录成功 {token}。")
        upload(token, filepath, filename)
    else:
        print("登录失败")
