BOT_API_TOKEN = '6029066878:AAEQM-TV8-VyAiRpuRApHiWE17Luwv_LsnY'
WEATHER_API_KEY = '06ef44d5c4cd1620557deef1b7414bfc'

CURRENT_WEATHER_API_CALL = (
        'https://api.openweathermap.org/data/2.5/weather?'
        'lat={latitude}&lon={longitude}&'
        'appid=' + WEATHER_API_KEY + '&units=metric'
)