import os
import requests
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

url = "https://api.weatherbit.io/v2.0/current"
api_key = "3e5551d00a2a4787a898a1ad24fefaeb"

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
    key_translate = "trnsl.1.1.20200330T171723Z.49e28c919bea6b43.832eb884575945784317a6d01b05cce3eabb7eaf"
    lang_from_to = "en-ru"
    
    payload = {
        "key": key_translate,
        "text": text,
        "lang": lang_from_to
    }
    response = requests.get(url=url_translate, params=payload)
    translation = ''.join(response.json()['text'])

    return translation

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1("Прогноз погоды"),
        html.Br()
    ],className='header'),

    html.Div([
        html.H4("Меня интересует погода в:"),
        dcc.Input(id="city-input", value="Москва", type="text"),
        html.Button(id='submit-button', n_clicks=0, children='Submit'),
        html.Br()
    ], className='user-input'),

    html.Div([
        html.Div([
            html.Img(id='weather-icon'),
            html.Div(id="weather-description")
        ], className='grid-item'),
        html.Div([
            html.Img(src=app.get_asset_url("thermometer.png")),
            html.Div(id="temperature")
        ], className='grid-item'),
        html.Div([
            html.Img(src=app.get_asset_url("humidity.png")),
            html.Div(id="humidity")
        ], className='grid-item'),
        html.Div([
            html.Img(src=app.get_asset_url("weathercock.png")),
            html.Div(id="wind")
        ], className='grid-item'),
        html.Div([
            html.Img(src=app.get_asset_url("barometer.png")),
            html.Div(id="pressure")
        ], className='grid-item'),
        html.Div([
            html.H4("Рекомендация:"),
            html.Div(id='recommendation')
        ], className='grid-item')
    ], className='grid-container'),

    html.Div([
        html.H5("Переведено сервисом «Яндекс.Переводчик» http://translate.yandex.ru")
    ])
])

@app.callback([Output('weather-description', 'children'),
               Output('temperature', 'children'),
               Output('humidity', 'children'),
               Output('wind', 'children'),
               Output('pressure', 'children'),
               Output('weather-icon', 'src'),
               Output('recommendation', 'children')],
              [Input('submit-button', 'n_clicks')],
              [State('city-input', 'value')])
def update_output(n_clicks, input):
    weather_data = get_weather(url, api_key, input)
    icon_path = weather_data['weather']['icon'] + '.png'
    rus_description = translate_weather(weather_data['weather']['description'])
    rus_wind = translate_weather(weather_data['wind_cdir_full'])
    press_mm = convert_pressure(weather_data['pres'])
    outfit = recommend_outfit(rus_description, weather_data['temp'], weather_data['wind_spd'])
    return(
        [
            "Сейчас {}".format(rus_description.lower()),
            "Температура воздуха {}°C, ощущается как {}°C".format(weather_data['temp'], weather_data['app_temp']),
            "Относительная влажность {}%".format(weather_data['rh']),
            "Ветер {}, скорость {:.2f} м/с.".format(rus_wind, weather_data['wind_spd']),
            "Атмосферное давление {} мм рт.ст.".format(press_mm),
            app.get_asset_url(icon_path),
            outfit
            ]
        )

if __name__ == '__main__':
    app.run_server(debug=True)