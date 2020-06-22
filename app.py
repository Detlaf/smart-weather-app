import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_functions import recommend_outfit, get_weather, convert_pressure, translate_weather

url = "https://api.weatherbit.io/v2.0/current"
api_key = "3e5551d00a2a4787a898a1ad24fefaeb"

app = dash.Dash(__name__)
server = app.server

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
    app.run_server()