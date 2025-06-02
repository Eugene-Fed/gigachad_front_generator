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
import argparse

PROMPT_FILE_NAME = Path("prompts/landing_rus.txt")
SYSTEM_PROMPT = SystemPrompt.RUS_EUGENE
CHAT_MODEL = LLModel.GIGACHAT_2_LITE
PAGES_PATH = Path("pages")
IS_STREAM = True  # Активация стриминга ответа от нейросети
VERIFY = Verify.false  # Может быть не только bool, но и конкретным значением
AI_RESPONSE_PATTERN = "```html"  # Определяем наличие "мусора" в теле ответа по форматированию текста нейронкой


def save_html(file_name, **kwargs):
    with open(file_name, "w", encoding='utf-8') as f:
        for bunch in get_text_response(**kwargs):
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
                      model: str,  # = LLModel.GIGACHAT_2_LITE
                      system_prompt: str,  # = SystemPrompt.RUS_EUGENE
                      stream: bool,  # = IS_STREAM
                      url: str = Url.CHAT_API) -> json:

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


def get_arguments(parser):
    # TODO указать лимит ожидания ответа для запроса без стриминга
    parser.add_argument("--prompt", "-p",
                        help="Set User prompt in quotes",
                        type=str,
                        default=None)
    parser.add_argument("--prompt_file", "-pf",
                        help="Set Path to file with user prompt",
                        type=str,
                        default=None)
    parser.add_argument("--sys_prompt", "-sp",
                        help="""Set System prompt in quotes. The model does not respond to the system prompt, 
                        add here the Context for the model's response or the Role to play in forming the response.""",
                        type=str,
                        default=None)
    parser.add_argument("--model", '-m',
                        help="Используемая сеть: lite, pro, max",
                        type=str,
                        default="lite",
                        choices=["lite", "pro", "max"])
    parser.add_argument("--output", "-o",
                        help="Имя файла, в который сохранится результат",
                        type=str,
                        default=None)
    parser.add_argument("--stream", "-s",
                        help="Возвращать результат сразу или по полной готовности",
                        type=bool,
                        default=IS_STREAM,
                        choices=[True, False])
    return parser.parse_args()


def parse_arguments(arguments) -> dict:
    parsed_arguments = dict()
    if prompt := arguments.prompt:
        parsed_arguments['user_prompt'] = prompt
    else:
        prompt_file = Path(arguments.prompt_file) if arguments.prompt_file else PROMPT_FILE_NAME
        with open(prompt_file, 'r', encoding='utf-8') as file:
            parsed_arguments['user_prompt'] = file.read()

    parsed_arguments['system_prompt'] = arguments.sys_prompt if arguments.sys_prompt else SYSTEM_PROMPT

    model = {"lite": LLModel.GIGACHAT_2_LITE,
             "pro": LLModel.GIGACHAT_2_PRO,
             "max": LLModel.GIGACHAT_2_MAX}
    parsed_arguments['model'] = model[arguments.model]

    pages_file_name = PAGES_PATH / f"index_{time.time()}_{parsed_arguments['model']}.html"
    parsed_arguments['file_name'] = Path(arguments.output) if arguments.output else pages_file_name

    parsed_arguments['stream'] = arguments.stream

    return parsed_arguments


def main():
    parser = argparse.ArgumentParser()
    parsed_arguments = parse_arguments(get_arguments(parser))

    load_dotenv()
    auth_key = os.getenv("GIGACHAT_AUTH_KEY")
    access_token, access_token_expires_time = get_access_token(auth_key=auth_key)
    print(f"Токен истекает: {datetime.fromtimestamp(access_token_expires_time)}")

    if not PAGES_PATH.is_dir():
        PAGES_PATH.mkdir()

    save_html(token=access_token,
              **parsed_arguments)
    clean_file(parsed_arguments["file_name"])


if __name__ == '__main__':
    main()
