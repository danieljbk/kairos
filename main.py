import os
import time
import smtplib
import requests
from datetime import datetime
from email.message import EmailMessage


def auto_import(module):
    try:
        exec(f"import {module}")  # check if module is installed
        # if so, module can be imported on the other file
        return f"import {module}"
    except ImportError:  # if module is not installed
        print(f"Automatically installing {module}...\n")
        try:
            # try using the pip command (works for some devices)
            os.system(f'python -m pip install {module}')
            print(f"Successfully installed {module}.")
        except ImportError:  # if the python command failed
            try:
                # use the pip3 command (works for most devices unless python is not installed)
                os.system(f'python -m pip3 install {module}')
                print(f"Successfully installed {module}.\n")
            except ImportError:
                print(f"ERROR: Failed to installed {module}.")
        # return the command to import the module on the other file
        return f"import {module}"


exec(auto_import("pyowm"))
exec(auto_import("schedule"))
exec(auto_import("uszipcode"))


# collect weather info and generate script to send in email
def weather(location, OPENWEATHERMAP_API_KEY):
    API_key = OPENWEATHERMAP_API_KEY

    if ", " in location or len(location) == 5:  # if location is name or zip code
        owm = pyowm.OWM(OPENWEATHERMAP_API_KEY)
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(location)
        w = observation.weather

        if ", " in location:  # location input was city, country
            city, country = location.split(", ")
        else:  # location input was zip code
            search = uszipcode.SearchEngine()
            location = search.by_zipcode(location)
            # needed to use "US" for country due to future code determining F˚/C˚
            city, country = location.city, "US"

        detailed_status = w.detailed_status
        if detailed_status == 'clear sky' or detailed_status == 'thunderstorm':
            detailed_status = f"a {detailed_status}"

        temp_data = []
        for x in w.temperature('fahrenheit').items():
            temp_data.append(x)
        temp_data = list(
            map(lambda x: temp_data[temp_data.index(x)][1], temp_data))[:-1]
        if country != 'US':
            # convert to Celsius
            temp_data = list(map(lambda x: (x - 32)/1.8, temp_data))
        temp_data = list(map(lambda x: int(round(x)), temp_data)
                         )  # round and get rid of decimals
        temp, max_temp, min_temp, feels_like = temp_data
        clouds = w.clouds
        humidity = w.humidity

    elif len(location) == 7:  # location input was city id
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_id = location
        final_url = base_url + "appid=" + API_key + "&id=" + city_id
        location_data = requests.get(final_url).json()
        weather_data = location_data['weather']
        city, country = location_data['name'], location_data['sys']['country']

        detailed_status = weather_data[0]['description']
        if detailed_status == 'clear sky' or detailed_status == 'thunderstorm':
            detailed_status = f"a {detailed_status}"

        temp = location_data['main']['temp']
        feels_like = location_data['main']['feels_like']
        min_temp = location_data['main']['temp_min']
        max_temp = location_data['main']['temp_max']
        pressure = location_data['main']['pressure']
        humidity = location_data['main']['humidity']
        clouds = location_data['clouds']['all']

        # converting weird temp input to normal Celcius
        temp_data = [temp, feels_like, min_temp, max_temp]
        temp_data = list(map(lambda x: x - 273, temp_data))
        if country == 'US':
            # convert to Fahrenheit
            temp_data = list(map(lambda x: x * (9/5) + 32, temp_data))
        temp_data = list(map(lambda x: round(x), temp_data))
        temp, feels_like, min_temp, max_temp = temp_data

    return city, country, detailed_status, clouds, humidity, temp, max_temp, min_temp, feels_like


def script(name, location, type, OPENWEATHERMAP_API_KEY):
    city, country, status, clouds, humidity, temp, max_temp, min_temp, feels_like = weather(
        location, OPENWEATHERMAP_API_KEY)

    if type == "email":
        script = ''
        hug_emoji, cloud_emoji, ok_emoji, heart_emoji = '🤗', '☁️', '👌', '💙'
        greeting = "Buenos días"
        if country == "US":
            degree_symbol = "˚F"
        else:
            degree_symbol = "˚C"
        bot_name = "~ καιρός"  # kairos in greek
    elif type == "sms":
        script = "\n"
        hug_emoji = cloud_emoji = ok_emoji = heart_emoji = ''
        greeting = "Buenos dias"
        degree_symbol = ' ' + "degrees"
        bot_name = "from Kairos"

    script += f"{greeting} {name}! {hug_emoji}\n"
    script += "\n"
    script += f"{city} is currently experiencing {status} with {clouds}% cloudiness. {cloud_emoji}\n"
    script += f"With {humidity}% humidity, it feels like {feels_like}{degree_symbol} outside. {ok_emoji}\n"
    script += "\n"
    script += f"Carpe diem!\n"
    script += f"{bot_name}\n"
    script += f"http://daniel.bio/projects/kairos {heart_emoji}"

    return script


def absolute_path(path):  # input relative path, output absolute path
    dirname = os.path.dirname(__file__)

    return os.path.join(dirname, path)


def gather_personal_data():  # from relative path assets/private
    OPENWEATHERMAP_API_KEY = open(absolute_path(
        "assets/personal/openweathermap_api_key.txt"), "r").readline().strip()
    GMAIL_USERNAME = open(absolute_path(
        "assets/personal/gmail_username.txt"), "r").readline().strip()
    GMAIL_API_KEY = open(absolute_path(
        "assets/personal/gmail_app_password.txt"), "r").readline().strip()

    return OPENWEATHERMAP_API_KEY, GMAIL_USERNAME, GMAIL_API_KEY


def gather_subscriber_data(subscription_type):
    path = absolute_path("assets/subscribers")
    path += "/" + subscription_type

    f = open(path, "r")
    subscribers = f.read().split("\n")
    f.close()

    for item in subscribers:
        if item == "UNSUBSCRIBED:":
            subscribers = subscribers[:subscribers.index(item)]
    # filter empty strings
    subscribers = list(filter(lambda item: item, subscribers))
    subscribers = list(map(lambda x: x.split(" & "), subscribers))

    return subscribers


def subscribers():  # list of addresses to send the email to
    email_subscribers = gather_subscriber_data("email.txt")
    sms_subscribers = gather_subscriber_data("sms.txt")

    return email_subscribers, sms_subscribers


# most important: for sending the email
def email_alert(to, subject, body, GMAIL_USERNAME, GMAIL_API_KEY):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    msg['from'] = GMAIL_USERNAME
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(GMAIL_USERNAME, GMAIL_API_KEY)
    server.send_message(msg)
    server.quit()


def today():  # collect today's date
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    date_time = datetime.fromtimestamp(timestamp)
    today = date_time.strftime("%d %B, %Y")

    return today


def send():  # send the email
    print(f"\nSending: {today()}\n")

    OPENWEATHERMAP_API_KEY, GMAIL_USERNAME, GMAIL_API_KEY = gather_personal_data()
    email_subscribers, sms_subscribers = subscribers()

    for data in email_subscribers:
        email_alert(data[0], f"What's the Weather Right Now? ({today()})", script(
            data[1], data[2], "email", OPENWEATHERMAP_API_KEY), GMAIL_USERNAME, GMAIL_API_KEY)

        if len(data[2]) == 5:  # if location input was zip code
            search = uszipcode.SearchEngine()
            data[2] = search.by_zipcode(data[2])
            data[2] = data[2].post_office_city  # turn zip code into city, state name
        elif len(data[2]) == 7:  # location input was city id
            API_key = OPENWEATHERMAP_API_KEY
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            city_id = data[2]
            final_url = base_url + "appid=" + API_key + "&id=" + city_id
            location_data = requests.get(final_url).json()
            weather_data = location_data['weather']
            city, country = location_data['name'], location_data['sys']['country']
            data[2] = city + ', ' + country
            
        print("    " + "- sent to:", data[0], "in", data[2])

    for data in sms_subscribers:
        email_alert(data[0], f"Weather Update ({today()})", script(
            data[1], data[2], "sms", OPENWEATHERMAP_API_KEY), GMAIL_USERNAME, GMAIL_API_KEY)

        if len(data[2]) == 5:  # if location input was zip code
            search = uszipcode.SearchEngine()
            data[2] = search.by_zipcode(data[2])
            data[2] = data[2].post_office_city  # turn zip code into city, state name
        elif len(data[2]) == 7:  # location input was city id
            API_key = OPENWEATHERMAP_API_KEY
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            city_id = data[2]
            final_url = base_url + "appid=" + API_key + "&id=" + city_id
            location_data = requests.get(final_url).json()
            weather_data = location_data['weather']
            city, country = location_data['name'], location_data['sys']['country']
            data[2] = city + ', ' + country
           
        print("    " + "- sent to:", data[0].split("@")[0], "in", data[2])


def run():
    now = datetime.now()
    if now.hour == 9 and now.minute == 0: # only send at 9AM
    	send()
    else:
        print("Wrong time!")

run()
