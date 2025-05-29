from datetime import datetime
from dotenv import load_dotenv
from gigachat_auth import get_access_token
from gigachat_params import Url, Scope, Verify, LLModel, Role, SYSTEM_PROMPT
from sse_stream import process_sse_stream
from pathlib import Path
import requests
import os
import json
import time

PROMPT_PATH = Path("prompt.txt")
PAGES_PATH = Path("pages")
CHAT_MODEL = LLModel.GIGACHAT_2_LITE
IS_STREAM = True  # Активация стриминга ответа от нейросети
VERIFY = Verify.false


def save_html():
    pass


def get_html():
    pass


def get_text_response(user_prompt: str,
                      token: str,
                      model: str = LLModel.GIGACHAT_2_LITE,
                      system_prompt: str = SYSTEM_PROMPT,
                      url: str = Url.CHAT_API,
                      stream: bool = IS_STREAM) -> json:
    '''
    payload = json.dumps({
        "model": "GigaChat-2-Max",
        "messages": [
            {
                "created_at": 1748374867,
                "role": "user",
                "content": "",
                "attachments": []
            },
            {
                "role": "assistant",
                "created_at": 1748374869,
                "content": ""
            }
        ],
        "profanity_check": True
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer <TOKEN>'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    '''
    payload = json.dumps(
        {
            "model": model,
            "messages": [
                {
                    "role": Role.SYSTEM,
                    "content": system_prompt
                },
                {
                    "role": Role.USER,
                    "content": user_prompt
                }
            ],
            "stream": stream,
            "update_interval": 0
        }
    ).encode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    if IS_STREAM:
        # response_text = ""
        # response_text += process_sse_stream("POST", url=url, headers=headers, data=payload, verify=VERIFY)
        # return response_text
        for bunch in process_sse_stream("POST", url=url, headers=headers, data=payload, verify=VERIFY):
            yield bunch
    else:
        response = requests.request("POST", url=url, headers=headers, data=payload, verify=VERIFY)
        return response.text


def main():
    load_dotenv()
    auth_key = os.getenv('GIGACHAT_AUTH_KEY')
    access_token, access_token_expires_time = get_access_token(auth_key=auth_key)
    with open(PROMPT_PATH, 'r', encoding='utf-8') as file:
        user_prompt = file.read()
    print(user_prompt)
    print(f"Токен истекает: {datetime.fromtimestamp(access_token_expires_time)}")

    with open(PAGES_PATH / f"index_{time.time()}.html",
              "w",
              encoding='utf-8') as f:
        for bunch in get_text_response(user_prompt="Напиши небольшой сайт на HTML+CSS",
                                       system_prompt="Строго выполняй запрос, без дополнительных комментариев",
                                       token=access_token, model=CHAT_MODEL):
            f.write(bunch)

    # response = get_text_response(user_prompt=user_prompt, token=access_token, model=CHAT_MODEL)
    # print(response)


if __name__ == '__main__':
    main()
