
import requests
import json

def recommend_outfit(description, temperature, wind):
    if 'дождь' in description:
        if wind <= 5:
            rec = "В такую погоду нужен дождевик или зонт"
        else:
            rec = "С таким ветром зонт не справится. Надевайте дождевик и резиновые сапоги"
    else:
        if temperature <= -10:
            rec = "Одевайтесь потеплее, понадобятся шапка и варежки"
        elif temperature > -10 and temperature <= 0:
            rec = "Без шапки лучше не выходить"
        elif temperature > 0 and temperature <= 10:
            rec = "Понадобится пальто или куртка"
        elif temperature > 10 and temperature <= 20:
            rec = "Тепло, достаточно плаща или ветровки"
        else:
            rec = "Пора доставать шорты и кепку"
    return rec

def get_weather(url, api_key, city_name):
    payload = {
        'key': api_key,
        'city': city_name
    }

    response = requests.get(url, params=payload)
    data = json.loads(response.text)

    return data['data'][0]

def convert_pressure(press_mbar):
    return round(0.75 * press_mbar)

def translate_weather(text):
    url_translate = "https://translate.yandex.net/api/v1.5/tr.json/translate"
    key_translate = ""
    lang_from_to = "en-ru"
    
    payload = {
        "key": key_translate,
        "text": text,
        "lang": lang_from_to
    }
    response = requests.get(url=url_translate, params=payload)
    translation = ''.join(response.json()['text'])

    return translation
