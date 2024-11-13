import os
import json
from urllib3.exceptions import InsecureRequestWarning
from key import Key

import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

api_url = os.getenv('API_URL')


def create_new_key(key_name):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    url = api_url + '/access-keys'
    error_message = ''
    r = requests.post(url, verify=False)  # Creating a new key
    if int(r.status_code) > 399:
        response = ("Что-то пошло не так.\nНе получилось создать ключ. Статус запроса: " + r.status_code)
        return response

    response = json.loads(r.text)
    key_id = response.get('id')
    access_url = response.get('accessUrl')

    rename_url = api_url + '/access-keys/' + key_id + '/name'
    r = requests.put(rename_url, data={'name': key_name}, verify=False)  # Renaming the key

    if int(r.status_code) > 399:
        error_message = ("Ключ создан, но не получилось его переименовать. Статус запроса: " + r.status_code)
    key = Key(key_id, key_name, access_url, error_message)
    return key


session = requests.Session()


def create_new_key_trial(key_name):
    """Создает ключ с ограничением на 10 Гб (Пробный вариант)"""
    url = api_url + '/access-keys'
    error_message = ''
    r = requests.post(url, verify=False)
    response = json.loads(r.text)
    key_id = response.get('id')
    access_url = response.get('accessUrl')
    key = Key(key_id, key_name, access_url, error_message)
    add_data_limit(key_id, 1024 ** 3 * 9.5)
    return key


def create_new_key_100(key_name):
    """Создает ключ с ограничением на 100 Гб"""
    url = api_url + '/access-keys'
    error_message = ''
    r = requests.post(url, verify=False)
    response = json.loads(r.text)
    key_id = response.get('id')
    access_url = response.get('accessUrl')
    key = Key(key_id, key_name, access_url, error_message)
    add_data_limit(key_id, 1024 ** 3 * 93.5)
    return key


def create_new_key_300(key_name):
    """Создает ключ с ограничением на 300 Гб"""
    url = api_url + '/access-keys'
    error_message = ''
    r = requests.post(url, verify=False)
    response = json.loads(r.text)
    key_id = response.get('id')
    access_url = response.get('accessUrl')
    key = Key(key_id, key_name, access_url, error_message)
    add_data_limit(key_id, 1024 ** 3 * 280)
    return key


def create_new_key_600(key_name):
    """Создает ключ с ограничением на 600 Гб"""
    url = api_url + '/access-keys'
    error_message = ''
    r = requests.post(url, verify=False)
    response = json.loads(r.text)
    key_id = response.get('id')
    access_url = response.get('accessUrl')
    key = Key(key_id, key_name, access_url, error_message)
    add_data_limit(key_id, 1024 ** 3 * 559)
    return key


def create_new_key_no_limit(key_name):
    """Создает ключ без ограничения"""
    url = api_url + '/access-keys'
    error_message = ''
    r = requests.post(url, verify=False)
    response = json.loads(r.text)
    key_id = response.get('id')
    access_url = response.get('accessUrl')
    key = Key(key_id, key_name, access_url, error_message)
    return key


def add_data_limit(key_id, limit_bytes):
    """Устанавливает ограничение на количество байт в ключе"""
    data = {"limit": {"bytes": limit_bytes}}
    response = session.put(f"{api_url}/access-keys/{key_id}/data-limit", json=data, verify=False)
    return response.status_code == 204
