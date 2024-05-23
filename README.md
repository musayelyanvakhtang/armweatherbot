# Weather Bot

Weather Bot is the first fully armenian Telegram bot written in Python. It uses PyTelegramBotAPI as a base and OpenWeatherMapAPI for weather data.
All information is provided in armenian, more languages and functions to be added in the future!

![image](https://i.imgur.com/P63Brzo.png)

## Installation

If you want to run the app locally, it is recommended to do so in a virtual environment since it has multiple requirements.

```bash
mkdir weatherbot
cd weatherbot
git clone https://github.com/musayelyanvakhtang/armweatherbot.git .
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
python bot.py
```

## Contributing
The bot uses DOTENV for personal information. You need to create an .env file manually.
```sh
BOT_KEY - Telegram Bot API Key
API_KEY - OpenWeatherMap API Key
DBNAME - PostgreSQL DB Name
DBUSER - PostgreSQL DB Userame
DBPASS - PostgreSQL DB Password
DBHOST - PostgreSQL DB Host
```

## Contributing

Pull requests are very welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

The program is licensed under [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html) and is free to download, use or distribute.