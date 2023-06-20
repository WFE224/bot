from coordinates import get_coordinates
from api_service import get_weather





def weather() -> str:
    """Returns a message about the temperature and weather description"""
    wthr = get_weather(get_coordinates())
    return f'{wthr.location}, {wthr.description}\n' \
           f'Температура на сегодня: {wthr.temperature}°C, по ощущениям: {wthr.temperature_feeling}°C Хорошего дня     （づ￣3￣）づ╭❤️～'


def wind() -> str:
    """Returns a message about wind direction and speed"""
    wthr = get_weather(get_coordinates())
    return f'{wthr.wind_direction} Ветер: {wthr.wind_speed} m/s'


def sun_time() -> str:
    """Returns a message about the time of sunrise and sunset"""
    wthr = get_weather(get_coordinates())
    return f'Bосход солнца: {wthr.sunrise.strftime("%H:%M")}\n' \
           f'Закат: {wthr.sunset.strftime("%H:%M")}\n'