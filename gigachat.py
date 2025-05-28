from datetime import datetime
from dotenv import load_dotenv
from gigachat_auth import get_access_token
from gigachat_params import Url, Scope, Verify, LLModels, SYSTEM_PROMPT
import requests
import os
import json
import time


def save_html():
    pass


def get_html():
    pass


def get_response(model: str = LLModels.GIGACHAT_2_MAX,
                 system_prompt: str = SYSTEM_PROMPT):
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
    payload = json.dumps({
        "model": model,
        "messages": [
            {
                "role": "assistant",
                "created_at": time.time(),
                "content": system_prompt
            },
            {
                "created_at": time.time(),
                "role": "user",
                "content": "",
                "attachments": []
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


def main():
    load_dotenv()
    auth_key = os.getenv('GIGACHAT_AUTH_KEY')
    access_token, access_token_expires_time = get_access_token(auth_key=auth_key)
    with open('prompt.txt', 'r', encoding='utf-8') as file:
        user_prompt = file.read()
    print(user_prompt)
    print(f"Токен истекает: {datetime.fromtimestamp(access_token_expires_time)}")


if __name__ == '__main__':
    main()
