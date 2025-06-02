from dotenv import load_dotenv, dotenv_values, set_key
from gigachat_params import Url, Scope, Verify
from time import time
import requests
import uuid
import base64
import json

ENV_PATH = ".env"


def get_b24_base_token(client_id: str = None, client_secret: str = None):
    # Исходная строка (должна быть в bytes)
    original_string = f"{client_id}:{client_secret}"
    original_bytes = original_string.encode('utf-8')  # Преобразуем строку в байты

    # Кодируем в base64
    base64_bytes = base64.b64encode(original_bytes)
    return base64_bytes.decode('utf-8')  # Преобразуем байты в строку


def get_access_token(auth_key: str = None,
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
    TODO - Если auth_key отсутствует, тогда используем get_b24_base_token()
    """

    # Проверяем .env на наличие действующего токена
    old_token = _get_access_token()
    if old_token:
        return old_token["token"], old_token["time"]

    # Если токен отсутствует или просрочен, получаем его по API
    print("Токен просрочен, запрашиваю новый.")

    if not auth_key:  # Можно получить из личного кабинета, или используя ID и секрет клиента в Личном кабинете
        # TODO - Какая-то проблема, API не принимает самогенерированный auth_key
        config = dotenv_values(ENV_PATH)
        client_id = config.get("GIGACHAT_CLIENT_ID")
        client_secret = config.get("GIGACHAT_CLIENT_SECRET")
        auth_key = get_b24_base_token(client_id=client_id, client_secret=client_secret)

    payload = {'scope': scope}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4()),
        'Authorization': f"Basic {auth_key}"
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=verify)

    print(response.text)
    access_token = json.loads(response.text).get('access_token')
    expires_time = json.loads(response.text).get('expires_at') / 1000  # API возвращает timestamp в миллисикундах
    _set_access_token(access_token, expires_time)
    return access_token, expires_time


def _set_access_token(access_token: str, expires_time: float):
    set_key(ENV_PATH, "ACCESS_TOKEN", access_token)
    set_key(ENV_PATH, "EXPIRES_TIME", str(expires_time))


def _get_access_token() -> dict:
    config = dotenv_values(ENV_PATH)
    expires_time = config.get("EXPIRES_TIME")  # Если токена нет в .env файле, пойдём получать его по API
    access_token = config.get("ACCESS_TOKEN")

    # Добавляем 1 секунду к текущему времени для перестраховки
    if expires_time and access_token and float(expires_time) > time() + 1.:
        return {"token": access_token,
                "time": float(expires_time)}


def main():
    import os
    from datetime import datetime
    load_dotenv()
    # access_token, expires_time = get_access_token(os.getenv('GIGACHAT_AUTH_KEY'))
    access_token, expires_time = get_access_token()
    print(f"Токен истекает: {datetime.fromtimestamp(expires_time)}")
    print(access_token)


if __name__ == '__main__':
    main()
