import os
import json


import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

api_url = os.getenv('API_URL')


def create_new_key(user_name):
    url = api_url + '/access-keys'
    r = requests.post(url, verify=False)  # Creating a new key
    if int(r.status_code) > 399:
        response = ("Что-то пошло не так, позовите Администратора.\nНе получилось создать ключ. Статус запроса: " +
                    r.status_code)
        return response

    response = json.loads(r.text)
    key_id = response.get('id')
    access_url = response.get('accessUrl')

    rename_url = api_url + '/access-keys/' + key_id + '/name'
    r = requests.put(rename_url, data={'name': user_name}, verify=False)  # Renaming the key
    if int(r.status_code) > 399:
        error_message = ("Ключ создан, но не получилось его переименовать. Статус запроса: " +
                         r.status_code + "Попробуйте воспользоваться ключом, возможно, он все же работает: ")
        return error_message + access_url
    return access_url

