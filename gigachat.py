from datetime import datetime
from dotenv import load_dotenv
from gigachat_auth import get_access_token
from gigachat_params import Url, Verify, LLModel, Role, SystemPrompt
from sse_stream import process_sse_stream
from pathlib import Path
import requests
import os
import json
import time

PROMPT_PATH = Path("prompts")
PROMPT_FILE_NAME = Path("landing_rus.txt")
PAGES_PATH = Path("pages")
CHAT_MODEL = LLModel.GIGACHAT_2_PRO
IS_STREAM = True  # Активация стриминга ответа от нейросети
VERIFY = Verify.false
AI_RESPONSE_PATTERN = "```html"  # Определяем наличие "мусора" в теле ответа по форматированию текста нейронкой


def save_html(file_name, user_prompt, token, model=CHAT_MODEL):
    with open(file_name, "w", encoding='utf-8') as f:
        for bunch in get_text_response(user_prompt=user_prompt, token=token, model=model):
            f.write(bunch)


def get_html():
    pass


def clean_file(file_path: str | Path, pattern: str = AI_RESPONSE_PATTERN):
    """
    Очистка файла от лишних символов, которые возвращает нейросеть.
    """
    file_path = Path(file_path)
    try:
        with open(file_path) as file:
            if not file.readline().startswith(pattern):
                print("\nФайл не был очищен, т.к. не найден паттерн форматированного текста")
                return  # Если файл начинается не с форматирования вывода нейросети, то пропускаем очистку

        content = file_path.read_text().splitlines()[1:-1]
        file_path.write_text('\n'.join(content))
        print("\nФайл был очищен")
    except IndexError:
        print("Файл содержит меньше 2 строк")
    except Exception as e:
        print("\n", e)


def get_text_response(user_prompt: str,
                      token: str,
                      model: str = LLModel.GIGACHAT_2_LITE,
                      system_prompt: str = SystemPrompt.RUS_EUGENE,
                      url: str = Url.CHAT_API,
                      stream: bool = IS_STREAM) -> json:

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
        for bunch in process_sse_stream("POST", url=url, headers=headers, data=payload, verify=VERIFY):
            yield bunch
    else:
        response = requests.request("POST", url=url, headers=headers, data=payload, verify=VERIFY)
        return response.text


def main():
    load_dotenv()
    auth_key = os.getenv('GIGACHAT_AUTH_KEY')
    access_token, access_token_expires_time = get_access_token(auth_key=auth_key)

    with open(PROMPT_PATH / PROMPT_FILE_NAME, 'r', encoding='utf-8') as file:
        user_prompt = file.read()
    print(f"Токен истекает: {datetime.fromtimestamp(access_token_expires_time)}")

    if not PAGES_PATH.is_dir():
        PAGES_PATH.mkdir()

    file_name = PAGES_PATH / f"index_{time.time()}_{CHAT_MODEL}.html"
    save_html(file_name=file_name, user_prompt=user_prompt, token=access_token, model=CHAT_MODEL)
    clean_file(file_name)


if __name__ == '__main__':
    main()
