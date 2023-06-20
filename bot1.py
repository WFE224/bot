import logging

from aiogram import Bot, Dispatcher, executor, types

import inline_keyboard
import messages
import config
BOT_API_TOKEN = '6029066878:AAEQM-TV8-VyAiRpuRApHiWE17Luwv_LsnY'
WEATHER_API_KEY = '06ef44d5c4cd1620557deef1b7414bfc'

CURRENT_WEATHER_API_CALL = (
        'https://api.openweathermap.org/data/2.5/weather?'
        'lat={latitude}&lon={longitude}&'
        'appid=' + WEATHER_API_KEY + '&units=metric'
)
logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'weather'])
async def show_weather(message: types.Message):
    await message.answer(text=messages.weather(),
                         reply_markup=inline_keyboard.WEATHER)


@dp.message_handler(commands='help')
async def show_help_message(message: types.Message):
    await message.answer(
        text=f'This bot can get the current weather from your IP address.',
        reply_markup=inline_keyboard.HELP)


@dp.message_handler(commands='wind')
async def show_wind(message: types.Message):
    await message.answer(text=messages.wind(), 
                         reply_markup=inline_keyboard.WIND)


@dp.message_handler(commands='sun_time')
async def show_sun_time(message: types.Message):
    await message.answer(text=messages.sun_time(), 
                         reply_markup=inline_keyboard.SUN_TIME)


@dp.callback_query_handler(text='weather')
async def process_callback_weather(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        text=messages.weather(),
        reply_markup=inline_keyboard.WEATHER
    )


@dp.callback_query_handler(text='wind')
async def process_callback_wind(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        text=messages.wind(),
        reply_markup=inline_keyboard.WIND
    )


@dp.callback_query_handler(text='sun_time')
async def process_callback_sun_time(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        text=messages.sun_time(),
        reply_markup=inline_keyboard.SUN_TIME
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

    from typing import Literal, TypeAlias
from urllib.request import urlopen
from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
import json

from coordinates import Coordinates
import config

Celsius: TypeAlias = float


class WindDirection(IntEnum):
    North = 0
    Northeast = 45
    East = 90
    Southeast = 135
    South = 180
    Southwest = 225
    West = 270
    Northwest = 315


@dataclass(slots=True, frozen=True)
class Weather:
    location: str
    temperature: Celsius
    temperature_feeling: Celsius
    description: str
    wind_speed: float
    wind_direction: str
    sunrise: datetime
    sunset: datetime


def get_weather(coordinates=Coordinates) -> Weather:
    """Requests the weather in OpenWeather API and returns it"""
    openweather_response = _get_openweather_response(
        longitude=coordinates.longitude, latitude=coordinates.latitude
    )
    weather = _parse_openweather_response(openweather_response)
    return weather


def _get_openweather_response(latitude: float, longitude: float) -> str:
    url = config.CURRENT_WEATHER_API_CALL.format(latitude=latitude, longitude=longitude)
    return urlopen(url).read()


def _parse_openweather_response(openweather_response: str) -> Weather:
    openweather_dict = json.loads(openweather_response)
    return Weather(
        location=_parse_location(openweather_dict),
        temperature=_parse_temperature(openweather_dict),
        temperature_feeling=_parse_temperature_feeling(openweather_dict),
        description=_parse_description(openweather_dict),
        sunrise=_parse_sun_time(openweather_dict, 'sunrise'),
        sunset=_parse_sun_time(openweather_dict, 'sunset'),
        wind_speed=_parse_wind_speed(openweather_dict),
        wind_direction=_parse_wind_direction(openweather_dict)
    )


def _parse_location(openweather_dict: dict) -> str:
    return openweather_dict['name']


def _parse_temperature(openweather_dict: dict) -> Celsius:
    return openweather_dict['main']['temp']


def _parse_temperature_feeling(openweather_dict: dict) -> Celsius:
    return openweather_dict['main']['feels_like']


def _parse_description(openweather_dict) -> str:
    return str(openweather_dict['weather'][0]['description']).capitalize()


def _parse_sun_time(openweather_dict: dict, time: Literal["sunrise", "sunset"]) -> datetime:
    return datetime.fromtimestamp(openweather_dict['sys'][time])


def _parse_wind_speed(openweather_dict: dict) -> float:
    return openweather_dict['wind']['speed']


def _parse_wind_direction(openweather_dict: dict) -> str:
    degrees = openweather_dict['wind']['deg']
    degrees = round(degrees / 45) * 45
    if degrees == 360:
        degrees = 0
    return WindDirection(degrees).name

from urllib.request import urlopen
from dataclasses import dataclass
import json


@dataclass(slots=True, frozen=True)
class Coordinates:
    latitude: float
    longitude: float


def get_coordinates() -> Coordinates:
    """Returns current coordinates using IP address"""
    data = _get_ip_data()
    latitude = data['loc'].split(',')[0]
    longitude = data['loc'].split(',')[1]

    return Coordinates(latitude=latitude, longitude=longitude)


def _get_ip_data() -> dict:
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    return json.load(response)

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

BTN_WEATHER = InlineKeyboardButton('Погода', callback_data='weather')
BTN_WIND = InlineKeyboardButton('Ветер', callback_data='wind')
BTN_SUN_TIME = InlineKeyboardButton('Рассвет и закат', 
                                    callback_data='sun_time')

WEATHER = InlineKeyboardMarkup().add(BTN_WIND, BTN_SUN_TIME)
WIND = InlineKeyboardMarkup().add(BTN_WEATHER).add(BTN_SUN_TIME)
SUN_TIME = InlineKeyboardMarkup().add(BTN_WEATHER, BTN_WIND)
HELP = InlineKeyboardMarkup().add(BTN_WEATHER, BTN_WIND).add(BTN_SUN_TIME)

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