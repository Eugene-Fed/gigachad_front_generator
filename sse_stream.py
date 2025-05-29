import json

import requests


def process_sse_stream(method, url, data, verify, headers=None):
    """
    Обрабатывает SSE-поток с заданного URL

    :param url: URL SSE-эндпоинта
    :param headers: Заголовки HTTP-запроса
    """
    try:
        with requests.request(method, url, headers=headers, data=data, verify=verify, stream=True) as response:
            response.raise_for_status()

            print("Получаем данные:")
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')

                    # Пропускаем комментарии и пустые строки
                    if decoded_line.startswith(':') or not decoded_line.strip():
                        continue

                    # Обработка SSE-события
                    if decoded_line.startswith('data:'):
                        data = decoded_line[5:].strip()
                        if data == "[DONE]":
                            break
                        content = json.loads(data)["choices"][0]["delta"]["content"]
                        print(content, end='')
                        yield content
                    elif decoded_line.startswith('event:'):
                        event_type = decoded_line[6:].strip()
                        print(f"Тип события: {event_type}")
                    elif decoded_line.startswith('id:'):
                        event_id = decoded_line[3:].strip()
                        print(f"ID события: {event_id}")
                    elif decoded_line.startswith('retry:'):
                        retry_time = int(decoded_line[6:].strip())
                        print(f"Время повторного подключения: {retry_time}ms")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при подключении к SSE-потоку: {e}")


def main():
    # Пример использования
    sse_url = 'https://example.com/events'
    process_sse_stream(sse_url)


if __name__ == '__main__':
    main()
