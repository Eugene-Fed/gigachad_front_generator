## gigachad_front_generator

### Как получить айдишники
https://developers.sber.ru/docs/ru/gigachat/quickstart/ind-create-project


### API Schema GigaChat
Находится в файле `schema/api.yml`

### Примеры сгенерированных страниц
Папка `page_examples`

### Разрешения
Код создаёт в папке проекта каталог `pages`, куда сохраняет все результаты в формате `index_<timestamp>_<model_name>.html`.  
Создайте эту папку заранее или разрешите коду доступ к созданию директорий в папке проекта.

### Рекомендация к генерации
- Используйте для тестирования модель `GigaChat-2` -- она же `GigaChat-2-Lite`, т.к. там большой запас токенов при небольшом расходе
- Используйте для проверки качества используйте модель не ниже `GigaChat-2-Pro`, т.к. `Lite` выдаёт посредственный результат

### Как получить токен доступа
https://developers.sber.ru/docs/ru/gigachat/api/reference/rest/post-token  
Время жизни токена: 30 минут

### Как получить SSL-сертификат
https://developers.sber.ru/docs/ru/gigachat/certificates

### Справка по API
https://developers.sber.ru/docs/ru/gigachat/api/reference/rest/post-ai-check


### Получить ответ от Модели
https://developers.sber.ru/docs/ru/gigachat/api/reference/rest/post-chat


### Потоговая генерация
https://developers.sber.ru/docs/ru/gigachat/guides/response-token-streaming?tool=python  
[Про SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#event_stream_format)

### История чата
https://developers.sber.ru/docs/ru/gigachat/guides/keeping-context

### Работа с функциями
https://developers.sber.ru/docs/ru/gigachat/guides/function-calling#rabota-s-sobstvennymi-funktsiyami

### Промт-инжиниринг
https://developers.sber.ru/docs/ru/gigachat/prompts-hub/prompt-engineering


### GigaChain (extension)
https://developers.sber.ru/docs/ru/gigachain/overview#quickstart