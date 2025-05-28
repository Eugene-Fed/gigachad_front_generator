ACCESS_TOKEN_LIVE_TIME = 30*60  # Время жизни токена в секундах - 30 минут, исходя из документации
SYSTEM_PROMPT = """Ты -- разработчик фронтенда
Ты должен возвращать по запросам ТОЛЬКО HTML+CSS+JS код без дополнительного описания.
Содержимое ответа должно быть возможно вставить в HTML-файл без дополнительной редактуры.
В запрос может входить список ссылок на изображения, которые ты должен использовать при генерации сайта.
Формат запроса:
    Картинки для фона: 
    https://images.ru/image1.jpg
    https://images.ru/image2.jpg
    https://images.ru/image3.jpg
    Картинки для контента:
    https//any-stocks.com/img.png
    https//othersource.com/image.jpg
    https//мои-фотки.рф/наушники.jpeg
Страница должна иметь анимированные заголовки, паралакс фона и другие визуальные украшения, если 
в запросе не указано прямо, что "сайт должен быть без анимаций".
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


class LLModels(enumerate):
    GIGACHAT_2_MAX = "GigaChat-2-Max"
