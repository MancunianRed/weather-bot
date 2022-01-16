from flask import Flask, request
import requests
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)

# {"ok": True} "<h1>Hello Igor</h1>"
# URL0 = "https://garik.pythonanywhere.com/"
# URL1 = "https://api.telegram.org/bot5018305864:AAHNTyksmRO_QVUeOd_z0ch3FwJmt-QeJ64/setWebhook?url=https://bb35-2001-56a-f972-8e00-6414-9280-8668-7998.ngrok.io"

thunderstorm = u'\U0001F4A8'    # Code: 200's, 900, 901, 902, 905
drizzle = u'\U0001F4A7'         # Code: 300's
rain = u'\U00002614'            # Code: 500's
snowflake = u'\U00002744'       # Code: 600's snowflake
snowman = u'\U000026C4'         # Code: 600's snowman, 903, 906
atmosphere = u'\U0001F301'      # Code: 700's foogy
clearSky = u'\U00002600'        # Code: 800 clear sky
fewClouds = u'\U000026C5'       # Code: 801 sun behind clouds
clouds = u'\U00002601'          # Code: 802-803-804 clouds general
hot = u'\U0001F525'             # Code: 904
defaultEmoji = u'\U0001F300'    # default emojis
wink = u'\U0001F609'            # wink emoji
smile = u'\U0001F642'           # smile emoji
telescope = u'\U0001F52D'       # telescope emoji


def getEmoji(weatherID):
    if weatherID:
        if str(weatherID)[0] == '2' or weatherID == 900 or weatherID==901 or weatherID==902 or weatherID==905:
            return thunderstorm
        elif str(weatherID)[0] == '3':
            return drizzle
        elif str(weatherID)[0] == '5':
            return rain
        elif str(weatherID)[0] == '6' or weatherID==903 or weatherID== 906:
            return snowflake + ' ' + snowman
        elif str(weatherID)[0] == '7':
            return atmosphere
        elif weatherID == 800:
            return clearSky
        elif weatherID == 801:
            return fewClouds
        elif weatherID==802 or weatherID==803 or weatherID==803:
            return clouds
        elif weatherID == 904:
            return hot
        else:
            return defaultEmoji    # Default emoji

    else:
        return defaultEmoji   # Default emoji


def send_message(chat_id, text):
    method = "sendMessage"
    token = "5018305864:AAHNTyksmRO_QVUeOd_z0ch3FwJmt-QeJ64"
    url = f"https://api.telegram.org/bot{token}/{method}"
    if text == f"Зато есть фото дня NASA {smile}":
        data = {"chat_id": chat_id, "text": text}
        requests.post(url, data=data)
    else:
        greeting_text = f"Hello " \
                        f"<b>{request.json['message']['chat']['first_name']}</b>"
        greeting_data = {"chat_id": chat_id, "text": greeting_text,
                         "parse_mode": 'HTML'}
        requests.post(url, data=greeting_data)
        data = {"chat_id": chat_id, "text": text}
        requests.post(url, data=data)


def send_sticker(chat_id):
    method_sticker = "sendSticker"
    method_message = "sendMessage"
    token = "5018305864:AAHNTyksmRO_QVUeOd_z0ch3FwJmt-QeJ64"
    url_sticker = f"https://api.telegram.org/bot{token}/{method_sticker}"
    url_message = f"https://api.telegram.org/bot{token}/{method_message}"
    sticker_id_LN = "CAACAgIAAxkBAAEDkW1hyUBFGOsQwDMTQuae0CoeQEW3bwACyQkAAn" \
                    "lc4glA7pA-2Jv6XyME"
    data = {"chat_id": chat_id, "sticker": sticker_id_LN}
    requests.post(url_sticker, data=data)
    data_message = {"chat_id": chat_id, "text": "Такого города у нас нет!!!"}

    requests.post(url_message, data=data_message)


def send_sticker_greeting(chat_id):
    method_sticker = "sendSticker"
    token = "5018305864:AAHNTyksmRO_QVUeOd_z0ch3FwJmt-QeJ64"
    url_sticker = f"https://api.telegram.org/bot{token}/{method_sticker}"
    sticker_id_ln = "CAACAgIAAxkBAAEDr6Vh4imK6XBbu3JdP1IwiX5ooAICiAACvQkAAnlc4gm9fAABvP4sJrojBA"
    data = {"chat_id": chat_id, "sticker": sticker_id_ln}
    requests.post(url_sticker, data=data)


def send_photo(chat_id, title, picture):
    token = "5018305864:AAHNTyksmRO_QVUeOd_z0ch3FwJmt-QeJ64"
    method = "sendPhoto"
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "photo": picture, "caption": title}
    requests.post(url, data=data)


def weather_info(chat_id):
    api_key = "5afa08972fc046476fa6a4f93513396d"
    try:
        city_name = request.json["message"]["text"]
        language_code = request.json["message"]["from"]["language_code"]
    except Exception:
        send_sticker(chat_id)
        send_message(chat_id, f"Зато есть фото дня NASA {smile}")
        send_photo(chat_id, nasa()[0], nasa()[1])
    else:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}" \
              f"&units=metric&lang={language_code}&appid={api_key}"
        res = requests.get(url)
        res_json = res.json()
        if res_json["cod"] == "404":
            send_sticker(chat_id)
            send_message(chat_id, f"Зато есть фото дня NASA {smile}")
            send_photo(chat_id, nasa()[0], nasa()[1])
        else:
            try:
                country = res_json["sys"]["country"]
                city = res_json['name']
                weather_text_mess = f"Current weather in {city} {country}\n"
            except Exception:
                weather_text_mess = f"Current weather in {city_name}\n"
            items_main = res_json["main"].items()
            for item in list(items_main)[0:2]:
                weather_text_mess += f"{item[0].capitalize():<20}{item[1]:.0f} C\n"
            weather_text_mess += f"{res_json['weather'][0]['description']} {getEmoji(res_json['weather'][0]['id'])}"
            send_message(chat_id, weather_text_mess)
            where_is_webb(chat_id)


def nasa():
    api_key = "QCxfgGcftzSC5YVCeqECDMnxZGe1pbgOACd5pmeR"
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    res = requests.get(url)
    res_json = res.json()
    title = res_json["title"]
    apod = res_json["url"]
    return title, apod


def where_is_webb(chat_id):
    url = "https://api.jwst-hub.com/track"
    res = requests.get(url)
    res_json = res.json()
    method = "sendMessage"
    token = "5018305864:AAHNTyksmRO_QVUeOd_z0ch3FwJmt-QeJ64"
    url_bot = f"https://api.telegram.org/bot{token}/{method}"
    webb_text = f"And, where is WEBB TELESCOPE? {telescope} \n\n" \
                f"{'Distance from Earth:':<32}{res_json['distanceEarthKm']:<12}km.\n" \
                f"{'Percentage completed:':<29}{res_json['percentageCompleted']:<14}%. \n" \
                f"{'Speed:':<45}{res_json['speedKmS']:<15}kms."
    webb_data = {"chat_id": chat_id, "text": webb_text,"parse_mode": 'HTML'}
    requests.post(url_bot, data=webb_data)
    send_photo(chat_id, res_json["currentDeploymentStep"], res_json["deploymentImgURL"])


@app.route('/', methods=["POST", "GET"])
def process():
    if request.method == "POST":
        r = request.get_json()
        chat_id = r["message"]["chat"]["id"]
        print(request.json)
        if r["message"]["text"] == "/start":
            text = f"I am a weather bot. Give me a city name and I'll reply with weather forecast and " \
                   "some interesting info from the space community."
            send_sticker_greeting(chat_id)
            send_message(chat_id, text)
        elif r["message"]["text"] == "/help":
            text = f"Just send a city name in english or russian to this bot and you'll get the current weather forecast.\n\n" \
                   f"I hope you will enjoy this simple bot\nFind a problem? Text me @GarikOds   {wink}"
            send_message(chat_id, text)
        else:
            weather_info(chat_id)
    return {"ok": True}


if __name__ == '__main__':
    app.run()
