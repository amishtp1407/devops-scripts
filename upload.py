#!/usr/bin/env python3

import os
import sys
import hashlib
import requests

def calculate_sha512(file_path):
    sha512_hash = hashlib.sha512()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            sha512_hash.update(chunk)
    return sha512_hash.hexdigest()

def compute_url(upload_uri, env):
    url = "https://license.haltdos.com"
    if env == "UAT":
        url = "https://license-uat.hltdos.com"

    url = url + upload_uri
    return url

def upload_file(file_path, version, env):
    try:
        file_hash = calculate_sha512(file_path)
        params = {
            'version': version,
            'description': 'github_master',
            'filename': file_path.split('/')[-1],
            'hash': file_hash
        }

        files = {'file': open(file_path, 'rb')}

        credentials = {
            "username" : os.environ.get(f'{env}_API_USERNAME'),
            "password" : os.environ.get(f'{env}_API_PASSWORD')
        }

        component_id = os.environ.get(f'{env}_COMPONENT_ID')
        upload_uri = f"/api/component/{component_id}"
        url = compute_url(upload_uri, env)

        print(f"Username: {credentials['username']} Password: {credentials['password']} Component ID: {component_id}")
        print(f"Uploading File {file_path} to {env} Env")
        response = requests.post(url, auth=(credentials["username"], credentials["password"]), files=files, data=params)
        if response.status_code == 200:
            print(f"Upload successful!")
        else:
            print(f"Failed to upload")
            sys.exit(1)

    except Exception as ex:
        print(f"Exception: {ex}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: ./upload.py <file_path> <version> <env>")
        sys.exit(1)

    file_path = sys.argv[1]
    version = sys.argv[2]
    env = sys.argv[3]

    upload_file(file_path, version, env)
