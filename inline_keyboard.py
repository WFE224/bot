from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

BTN_WEATHER = InlineKeyboardButton('Погода', callback_data='weather')
BTN_WIND = InlineKeyboardButton('Ветер', callback_data='wind')
BTN_SUN_TIME = InlineKeyboardButton('Рассвет и закат', 
                                    callback_data='sun_time')

WEATHER = InlineKeyboardMarkup().add(BTN_WIND, BTN_SUN_TIME)
WIND = InlineKeyboardMarkup().add(BTN_WEATHER).add(BTN_SUN_TIME)
SUN_TIME = InlineKeyboardMarkup().add(BTN_WEATHER, BTN_WIND)
HELP = InlineKeyboardMarkup().add(BTN_WEATHER, BTN_WIND).add(BTN_SUN_TIME)