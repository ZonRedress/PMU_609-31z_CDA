import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Напиши мне название города, и я пришлю текущую погоду. Например: Москва")

@dp.message()
async def get_weather(message: types.Message):
    city_name = message.text.strip()
    
    # API OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&lang=ru&units=metric&appid={WEATHER_API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            await message.answer("❌ Город не найден. Попробуйте написать название по-другому.")
            return

        # Извлекаем нужные данные из ответа JSON
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        answer = (
            f"🌍 Город: {city_name.capitalize()}\n"
            f"🌡️ Температура: {temp}°C\n"
            f"🤔 Ощущается как: {feels_like}°C\n"
            f"☁️ Погода: {description}\n"
            f"💧 Влажность: {humidity}%\n"
            f"💨 Ветер: {wind_speed} м/с"
        )
        await message.answer(answer)

    except Exception as e:
        await message.answer("⚠️ Произошла ошибка при получении данных о погоде.")
        print(f"Ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())