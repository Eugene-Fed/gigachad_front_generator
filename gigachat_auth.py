from dotenv import load_dotenv
from gigachat_params import Url, Scope, Verify
import requests
import uuid
import base64
import json


def get_b24_base_token(client_id: str, client_secret: str):
    # Исходная строка (должна быть в bytes)
    original_string = f"{client_id}:{client_secret}"
    original_bytes = original_string.encode('utf-8')  # Преобразуем строку в байты

    # Кодируем в base64
    base64_bytes = base64.b64encode(original_bytes)
    return base64_bytes.decode('utf-8')  # Преобразуем байты в строку


def get_access_token(auth_key: str,
                     scope: str = Scope.GIGACHAT_API_PERS,
                     url: str = Url.AUTH_API,
                     verify=Verify.false,
                     ) -> tuple:
    """
    Получить токен авторизации HTTP-запросов в апи GigaChat. Время жизни токена: 30 минут
    :param auth_key: Нужен для получения токена доступа Access token - https://vk.cc/cMnjhs
    :param scope: Вариант API: для физ лиц, для ИП и юрлиц с предоплатой или с оплатой по факту
    :param url:
    :param verify: https://developers.sber.ru/docs/ru/gigachat/certificates
    :return: str: Токен доступа, float: Время истечения токена в секундах
    """
    payload = {'scope': scope}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4()),
        'Authorization': f"Basic {auth_key}"
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=verify)

    access_token = json.loads(response.text).get('access_token')
    expires_time = json.loads(response.text).get('expires_at') / 1000  # API возвращает timestamp в миллисикундах
    return access_token, expires_time


def main():
    import os
    from datetime import datetime
    load_dotenv()
    _, expires_time = get_access_token(os.getenv('GIGACHAT_AUTH_KEY'))
    print(f"Токен истекает: {datetime.fromtimestamp(expires_time)}")


if __name__ == '__main__':
    main()
