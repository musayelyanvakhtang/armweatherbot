import telebot
import requests
import psycopg2
from datetime import datetime


bot = telebot.TeleBot('')
api_key = ""

def emojy(weather):
    if weather=="Thunderstorm":
        return "⚡️"
    elif weather=="Drizzle":
        return "🌦"
    elif weather=="Rain":
        return "⛈"
    elif weather=="Snow":
        return "❄️"
    elif weather=="Clear":
        return "☀️"
    elif weather=="Clouds":
        return "☁️"
    else:
        return "🌪"
    
def translate(main):
    if main== "Thunderstorm":
        return "Ամպրոպ"
    elif main == "Drizzle":
        return "Թույլ անձրև"
    elif main== "Rain":
        return "Անձրև"
    elif main == "Snow":
        return "Ձյուն"
    elif main == "Clear":
        return "Արև"
    elif main == "Clouds":
        return "Ամպամած"
    else:
        return "Փոթորիկ"
    
def timestamp_to_date(ts):
    return datetime.fromtimestamp(ts).strftime("%H:%M")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🌤️")
    bot.send_message(message.chat.id, "Ողջույն! ☀️🌻\nԵս կարող եմ ցուցադրել եղանակային տվյալներ քո ուզած քաղաքի մասին։ 🏙️🌞\nՈւղղակի մուտքագրիր այն լատինատառ։")

    tid = message.chat.id
    username = message.from_user.username
    name = ""
    lname = ""
    if message.from_user.first_name:
        name = message.from_user.first_name
    if message.from_user.last_name:
        lname = message.from_user.last_name

    # to ENV
    conn = psycopg2.connect(
        dbname="",
        user="",
        password="",
        host=""
    )
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id BIGINT PRIMARY KEY, username VARCHAR(50) NOT NULL, name VARCHAR(80) NOT NULL)")
    conn.commit()
    cursor.execute("INSERT INTO users (id, username, name) VALUES ('%s', '%s', '%s') ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, username = EXCLUDED.username" % (tid, username, name+" "+lname)) 
    conn.commit()
    conn.close()

@bot.message_handler(content_types=["text"])
def get_weather(message):
    city = message.text.strip().title()
    hasce="https://api.openweathermap.org/data/2.5/weather"
    parameters = {"q": city, "appid": api_key, "units": "metric"}
    weather_info = requests.get(hasce, params=parameters)
    if weather_info.status_code == 404:
        bot.send_message(message.chat.id,"Ցավոք, այդ քաղաքը չի գտնվել։ Խնդրում եմ մուտքագրեք նոր քաղաքի անուն։")
    else:
        weather_info=weather_info.json()

        main=weather_info["weather"][0]["main"]
        temp=weather_info["main"]["temp"]
        feels_like = weather_info["main"]["feels_like"]
        pressure = weather_info["main"]["pressure"]
        humidity = weather_info["main"]["humidity"]

        perception = ""
        if "rain" in weather_info.keys():
            perception = weather_info["rain"]["1h"]

        visibility = weather_info["visibility"]
        cloudiness = weather_info["clouds"]["all"]
        wind_speed = weather_info["wind"]["speed"]

        sunrise = timestamp_to_date(weather_info["sys"]["sunrise"])
        sunset = timestamp_to_date(weather_info["sys"]["sunset"])


        bot.send_message(message.chat.id, emojy(main))
        bot.send_message(message.chat.id, translate(main))
        
        weather_message = f"Այս պահին ջերմաստիճանը: {temp}°C\n"
        weather_message += f"Զգացվում է որպես {feels_like}°C\n\n"
        weather_message += f"📊 Մթնոլորտային ճնշումը։ {pressure} Պա\n"
        weather_message += f"💧 Օդի խոնավությունը: {humidity} %\n"
        if perception:
            weather_message += f"🌧️ Տեղումներ։ {perception} մմ\n"
        weather_message += f"\n🛣️ Տեսանելիություն։ {visibility} մ\n"
        weather_message += f"☁️ Ամպամածություն։ {cloudiness} %\n"
        weather_message += f"🍃 Քամու արագություն։ {wind_speed} մ/վրկ\n\n"
        weather_message += f"🌅 Արևածագ։ {sunrise}\n"
        weather_message += f"🌇 Մայրամուտ։ {sunset}"

        bot.send_message(message.chat.id, weather_message)

bot.infinity_polling()