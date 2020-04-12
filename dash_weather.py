import os
import requests
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

url = "https://api.weatherbit.io/v2.0/current"
api_key = "3e5551d00a2a4787a898a1ad24fefaeb"

def get_weather(url, api_key, city_name):
    payload = {
        'key': api_key,
        'city': city_name
    }

    res = requests.get(url, params=payload)
    data = json.loads(res.text)

    return data['data'][0]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1("Прогноз погоды"),
        html.Br()
    ],className='header'),

    html.Div([
        dcc.Input(id="city-input", value="Moscow", type="text"),
        html.Button(id='submit-button', n_clicks=0, children='Submit'),
        html.Br()
    ], className='user-input'),

    html.Div([
        html.Div(id="weather-description"),
        html.Div(id="temperature"),
        html.Div(id="humidity"),
        html.Div(id="wind"),
        html.Div(id="pressure"),
        html.Div([
            html.Img(id='weather-icon')
        ])
    ], className='results-output')
])

@app.callback([Output('weather-description', 'children'),
               Output('temperature', 'children'),
               Output('humidity', 'children'),
               Output('wind', 'children'),
               Output('pressure', 'children'),
               Output('weather-icon', 'src')],
              [Input('submit-button', 'n_clicks')],
              [State('city-input', 'value')])
def update_output(n_clicks, input):
    weather_data = get_weather(url, api_key, input)
    icon_path = weather_data['weather']['icon'] + '.png'
    return(
        [
            "Сегодня {}".format(weather_data['weather']['description']),
            "Температура воздуха {}°C, ощущается как {}°C".format(weather_data['temp'], weather_data['app_temp']),
            "Относительная влажность {}%".format(weather_data['rh']),
            "Ветер {}, скорость {:.2f} м/с.".format(weather_data['wind_cdir_full'], weather_data['wind_spd']),
            "Атмосферное давление {} мбар".format(weather_data['pres']),
            app.get_asset_url(icon_path)
        ]
    )

if __name__ == '__main__':
    app.run_server(debug=True)