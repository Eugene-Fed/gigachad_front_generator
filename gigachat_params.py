ACCESS_TOKEN_LIVE_TIME = 30*60  # Время жизни токена в секундах - 30 минут, исходя из документации


class SystemPrompt(enumerate):
    ENG_VALENTINE = """You must return ONLY HTML+CSS+JS code in response to requests, without any additional description.
    The response content should be ready to paste into an HTML file without any additional editing.
    Build a modern dark-themed landing page, it should have a developer aesthetic feeling like on
    https://operahsg.com/en/
    https://refraction.dev/
    https://evervault.com/
    https://www.gblagency.be/
    The page should also feature fluid animations, glassmorphism and spotlight effect.
    Your output should be a single code block with index.html (<style> for CSS, <script> for JS), no other text is allowed.
    Write text on Russian.
    """
    RUS_EUGENE = """Ты -- разработчик фронтенда
    Ты должен возвращать по запросам ТОЛЬКО HTML+CSS+JS код без дополнительного описания.
    Содержимое ответа должно быть возможно вставить в HTML-файл без дополнительной редактуры.
    Страница должна иметь анимированные заголовки, паралакс фона и другие визуальные украшения, если 
    в запросе не указано прямо, что "сайт должен быть без анимаций".
    В запрос может входить список ссылок на изображения, которые ты должен использовать при генерации сайта.
    Не используй форматирование при выводе в виде ```html в начале и ``` в конце текста
    Формат запроса:
        Картинки для фона: 
        https://images.ru/image1.jpg
        https://images.ru/image2.jpg
        https://images.ru/image3.jpg
    
        Картинки для контента:
        https//any-stocks.com/img.png
        https//othersource.com/image.jpg
        https//мои-фотки.рф/наушники.jpeg
    """
    RUS_REACT = """Ты -- разработчик фронтенда
    Ты должен возвращать по запросам ТОЛЬКО REACT код без дополнительного описания.
    Содержимое ответа должно быть возможно вставить в JSX-файл без дополнительной редактуры.
    Страница должна иметь плавные анимации, эффект стекломорфизма, точечную подсветку и другие визуальные украшения,
    если в запросе не указано прямо, что "сайт должен быть без анимаций".
    В запрос может входить список ссылок на изображения, которые ты должен использовать при генерации сайта.
    Не используй форматирование при выводе в виде ```html в начале и ``` в конце текста
    Формат запроса:
        Картинки для фона: 
        https://images.ru/image1.jpg
        https://images.ru/image2.jpg
        https://images.ru/image3.jpg

        Картинки для контента:
        https//any-stocks.com/img.png
        https//othersource.com/image.jpg
        https//мои-фотки.рф/наушники.jpeg
    """


class Url(enumerate):
    """
    AUTH_API - для получения access_token
    CHAT_API - для отправки запросов в чат
    """
    AUTH_API = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    CHAT_API = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"


class Scope(enumerate):
    """
    GIGACHAT_API_PERS - версия API для физических лиц
    GIGACHAT_API_B2B - доступ для ИП и юридических лиц по предоплате
    GIGACHAT_API_CORP - доступ для ИП и юридических лиц по схеме pay-as-you-go
    """
    GIGACHAT_API_PERS = 'GIGACHAT_API_PERS'
    GIGACHAT_API_B2B = 'GIGACHAT_API_B2B'
    GIGACHAT_API_CORP = 'GIGACHAT_API_CORP'


class Verify(enumerate):
    """
    SSL-сертификат Сбера не доверен, реквест не пропускает запрос. Решить другим способом
    false - Выключение SSL в requests
    Подробнее в документации https://developers.sber.ru/docs/ru/gigachat/certificates
    """
    false = False
    # TODO - доописать другие варианты


class LLModel(enumerate):
    GIGACHAT_2_MAX = "GigaChat-2-Max"
    GIGACHAT_2_PRO = "GigaChat-2-Pro"
    GIGACHAT_2_LITE = "GigaChat-2"
    EMBEDDINGS_GIGA_R = "EmbeddingsGigaR"  # Векторное представление текстов - продвинутая модель
    GIGACHAT_MAX = "GigaChat-Max"
    GIGACHAT_PRO = "GigaChat-Pro"
    GIGACHAT_LITE = "GigaChat"
    GIGACHAT_PLUS = "GigaChat-Plus"  # Вероятно более не поддерживается
    GIGACHAT_2_MAX_PREVIEW = "GigaChat-2-Max-preview"  # Модель в раннем доступе
    EMBEDDINGS_2 = "Embeddings-2"  # Векторное представление текстов


class Role(enumerate):
    """
    SYSTEM: системный промпт, который задает роль модели, например, должна модель отвечать как академик или как школьник
    USER: сообщение пользователя
    ASSISTANT: ответ модели
    FUNCTION: сообщение с результатом работы пользовательской функции https://vk.cc/cMnXEQ
    """
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"
