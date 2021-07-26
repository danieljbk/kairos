import os
import time
import smtplib
from datetime import datetime
from email.message import EmailMessage

# auto-import modules that require additional installation
try:
    import pyowm
except ImportError:
    print("Automatically installing the pyowm module...\n")
    try:
        os.system('python -m pip install pyowm')
        print("Successfully installed.")
    except ImportError:
        os.system('python -m pip3 install pyowm')
        print("Successfully installed.\n")
        
try:
    import schedule
except ImportError:
    print("Automatically installing the schedule module...\n")
    try:
        os.system('python -m pip install schedule')
        print("Successfully installed.")
    except ImportError:
        os.system('python -m pip3 install schedule')
        print("Successfully installed.\n")

# after installing, actually import the modules
import pyowm
import schedule


def weather(location, OPENWEATHERMAP_API_KEY): # collect weather info and generate script to send in email
    city, country = location.split(", ")

    owm = pyowm.OWM(OPENWEATHERMAP_API_KEY)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(location)
    w = observation.weather
    
    detailed_status = w.detailed_status
    if detailed_status == 'clear sky' or detailed_status == 'thunderstorm':
        detailed_status = f"a {detailed_status}"
    
    temp_data = []
    for x in w.temperature('fahrenheit').items():
        temp_data.append(x)
    temp_data = list(map(lambda x: temp_data[temp_data.index(x)][1], temp_data))[:-1]
    if country != 'US':
        temp_data = list(map(lambda x: (x - 32)/1.8, temp_data)) # convert to Celsius
    temp_data = list(map(lambda x: int(round(x)), temp_data)) # round and get rid of decimals
    temp, max_temp, min_temp, feels_like = temp_data
    
    return city, country, detailed_status, w.clouds, w.humidity, temp, max_temp, min_temp, feels_like


def script(name, location, type, OPENWEATHERMAP_API_KEY):
    city, country, status, clouds, humidity, temp, max_temp, min_temp, feels_like = weather(location, OPENWEATHERMAP_API_KEY)
    
    if type == "email":
        script = ''
        hug_emoji, cloud_emoji, ok_emoji, heart_emoji = '🤗', '☁️', '👌', '💙'
        greeting = "Buenos días"
        if country == "US":
            degree_symbol = "˚F"
        else:
            degree_symbol = "˚C"
        bot_name = "~ καιρός" # kairos in greek
    elif type == "sms":
        script = "\n"
        hug_emoji = cloud_emoji = ok_emoji = heart_emoji = ''
        greeting = "Buenos dias"
        degree_symbol = ' ' + "degrees"
        bot_name = "from Kairos"

    script += f"{greeting} {name}! {hug_emoji}\n"
    script +=  "\n"
    script += f"{city} is currently experiencing {status} with {clouds}% cloudiness. {cloud_emoji}\n"
    script += f"With {humidity}% humidity, it feels like {feels_like}{degree_symbol} outside. {ok_emoji}\n"
    script +=  "\n"
    script += f"Carpe diem!\n"
    script += f"{bot_name}\n"
    script += f"http://daniel.bio/kairos {heart_emoji}"
    
    return script


def absolute_path(path): # input relative path, output absolute path
    dirname = os.path.dirname(__file__)
    
    return os.path.join(dirname, path)


def gather_personal_data(): # from relative path assets/private
    OPENWEATHERMAP_API_KEY = open(absolute_path("assets/personal/openweathermap_api_key.txt"), "r").readline().strip()
    GMAIL_USERNAME = open(absolute_path("assets/personal/gmail_username.txt"), "r").readline().strip()
    GMAIL_API_KEY = open(absolute_path("assets/personal/gmail_app_password.txt"), "r").readline().strip()
    
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
    subscribers = list(filter(lambda item: item, subscribers)) # filter empty strings
    subscribers = list(map(lambda x: x.split(" & "), subscribers))
    
    return subscribers


def subscribers(): # list of addresses to send the email to
    email_subscribers = gather_subscriber_data("email.txt")
    sms_subscribers = gather_subscriber_data("sms.txt")
    
    return email_subscribers, sms_subscribers


def email_alert (to, subject, body, GMAIL_USERNAME, GMAIL_API_KEY): # most important: for sending the email
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


def today(): # collect today's date
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    date_time = datetime.fromtimestamp(timestamp)
    today = date_time.strftime("%d %B, %Y")

    return today


def send(): # send the email
    print(f"\nSending: {today()}\n")

    OPENWEATHERMAP_API_KEY, GMAIL_USERNAME, GMAIL_API_KEY = gather_personal_data()
    email_subscribers, sms_subscribers = subscribers()
    
    for data in email_subscribers:
        email_alert(data[0], f"What's the Weather Right Now? ({today()})", script(data[1], data[2], "email", OPENWEATHERMAP_API_KEY), GMAIL_USERNAME, GMAIL_API_KEY)
        print("    " + "- sent to:", data[0], "in", data[2])
    
    for data in sms_subscribers:
        email_alert(data[0], f"Weather Update ({today()})", script(data[1], data[2], "sms", OPENWEATHERMAP_API_KEY), GMAIL_USERNAME, GMAIL_API_KEY)
        print("    " + "- sent to:", data[0].split("@")[0], "in", data[2])

    print(f"\nSuccess: {today()}\n")


def run(): # schedule the email to send every day at a specific time
    print("When should the email be sent out? (9PM would be 21:00, and 1AM would be 01:00)")
    hour = input("    Hour: ")
    minute = input("    Minute: ")
    print()
    
    if hour:
        hour = int(hour)
    else: 
        hour = 0
    
    if minute:
        minute = int(minute)
    else: 
        minute = 0
    
    am_pm = 'AM'
    if hour >= 12:
        am_pm = 'PM'
    
    designated_time = f"{hour}:{minute}"
    if hour < 10:
        hour = f"0{hour}"
    if minute < 10:
        minute = f"0{minute}"
    designated_time = f"{hour}:{minute}"
    
    print()
    print(f"Kairos scheduled to send at {int(hour)}:{minute}{am_pm}...")
    print()
    schedule.every().day.at(designated_time).do(send)
    while True:
        print("    " + "- checking in:", datetime.now().time())
        schedule.run_pending()
        send() # uncomment to send immediately (for testing)
        time.sleep(1500)


run()
