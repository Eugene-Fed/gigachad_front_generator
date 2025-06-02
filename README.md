## gigachad_front_generator

### Подготовка к запуску
1. Зарегистрироваться на [сайте разработчиков](https://developers.sber.ru/studio/workspaces/) или авторизоваться со Сбер ID
1. Создать проект GigaChat API: https://disk.yandex.ru/i/pEw-eYPcyPLEjg
1. Войти в созданное Рабочее пространство и открыть API ключи: https://disk.yandex.ru/i/RtKqiF00zmxQlA
1. Создать Ключ авторизации: https://disk.yandex.ru/i/PlT0EfJ015KUQw
1. Указать Ключ авторизации как значение переменной окружения `GIGACHAT_AUTH_KEY` (в системе или в файле `.env`)  
   
Другие ключи не требуются для дальнейшей работы, т.к. код получает Токен доступа и сохраняет его в `.env`-файл

### Установите зависимости
`pip install -r requirements.txt`

### Разрешения
Код создаёт в папке проекта каталог `pages`, куда сохраняет все результаты в формате `index_<timestamp>_<model_name>.html`.  
Создайте эту папку заранее или разрешите коду доступ к созданию директорий в папке проекта.

### Запуск
`python gigachat.py` - Запуск со стандартным Промптом и настройками  

### Настройки по-умолчанию
#### user_prompt
Промт хранится в файле `prompts/landing_rus.txt`.  
Изменить файл, в котором хранится промпт можно командой `-pf` / `--prompt_file`
```python
python gigachat.py -pf prompts/another_super_cool_prompt.txt
```
Также возможно указать пользовательский промт непосредственно при запуске с помощью параметра `-p` / `--prompt`
```python
python gigachat.py -p "Запили крутой лендинг с тёмной темой."
```
Приоритет выбора промпта (в порядке убывания):
1. Промт в консоли `-p`
1. Промт в указанном файле `-pf`
1. Промт в стандартном файле, указанный в константе `PROMPT_FILE_NAME` модуля `gigachat.py`

#### system_prompt
Системные промпты хранятся в `gigachat_params.py` как константы класса `SystemPrompt`.  
Можно добавить свой системный промт как новую константу этого класса, после чего установить новое значение по-умолчанию в константу `SYSTEM_PROMPT` модуля `gigachat.py`

Системный промпт также можно указать при запуске кода через параметр `-sp` / `--system_prompt`
```python
python gigachat.py -sp "Ты -- разработчик фронтенда. Ты должен возвращать по запросам ТОЛЬКО HTML+CSS+JS код без дополнительного описания."
```

#### models
На выбор доступны 3 модели: `lite`, `pro`, `max`. Без параметров будет использована `lite` модель, для указания нужной используйте параметр `-m` / `--model`
```python
python gigachat.py -m pro
```

#### output_file
Результат сохраняется в папке `pages`. Имя файла по-умолчанию имеет формат `index_<timestamp>_<model_name>.html`  

Изменить имя файла, в который сохранится результат, можно через параметр `-o`, `--output` 
Пример:
```python
python gigachat.py -o my_file.txt
```
Примеры сгенерированных страниц находятся в папке `page_examples`.

#### stream
Параметр `-s` / `--stream` отвечает за формат отдачи результата работы нейронкой.
- `True` -- API работает в режиме стриминга ответа (значение по-умолчанию)
- `False` -- API возвращает только полный ответ по готовности (ожидание может занять длительное время)

### Рекомендация к генерации
- Используйте для тестирования модель `GigaChat-2` -- она же `GigaChat-2-Lite`, т.к. там большой запас токенов при небольшом расходе
- Используйте для проверки качества модель не ниже `GigaChat-2-Pro`, т.к. `Lite` выдаёт посредственный результат

### API Schema GigaChat
Находится в файле `schema/api.yml`

### Ссылки на документацию для разработчиков
- [Типичные статус-ошибки GigaChat API](https://developers.sber.ru/docs/ru/gigachat/api/errors-description?responseCode=400)
- [Quick Start](https://developers.sber.ru/docs/ru/gigachat/quickstart/ind-create-project)
- [Как получить токен доступа](https://developers.sber.ru/docs/ru/gigachat/api/reference/rest/post-token). Время жизни токена: 30 минут
- [Как получить сертификат](https://developers.sber.ru/docs/ru/gigachat/certificates). Текущая версия работает без SSL
- [Справка по API](https://developers.sber.ru/docs/ru/gigachat/api/reference/rest/post-ai-check)
- [Получить ответ от Модели](https://developers.sber.ru/docs/ru/gigachat/api/reference/rest/post-chat)
- [Потоговая генерация](https://developers.sber.ru/docs/ru/gigachat/guides/response-token-streaming?tool=python)  
- [Про SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#event_stream_format)
- [История чата](https://developers.sber.ru/docs/ru/gigachat/guides/keeping-context)
- [Работа с функциями](https://developers.sber.ru/docs/ru/gigachat/guides/function-calling#rabota-s-sobstvennymi-funktsiyami)
- [Промт-инжиниринг](https://developers.sber.ru/docs/ru/gigachat/prompts-hub/prompt-engineering)
- [GigaChain](https://developers.sber.ru/docs/ru/gigachain/overview#quickstart) (extension)
