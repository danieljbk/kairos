import smtplib
import pyowm
import schedule
import time
from email.message import EmailMessage
from datetime import datetime


def weather(location): # collect weather info and generate script to send in email
    city, country = location.split(", ")

    owm = pyowm.OWM(OPENWEATHERMAP_API_KEY) # github secret
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


def script(name, location, type):
    city, country, status, clouds, humidity, temp, max_temp, min_temp, feels_like = weather(location)
    
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


def gather_data(subscription_type):
    path = "/Users/danielkwon/Library/Mobile Documents/com~apple~CloudDocs/Daniel's Files/Coding/VSCode/Python/Kairos/assets/subscribers/"
    path += subscription_type

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
    email_subscribers = gather_data("email")
    sms_subscribers = gather_data("sms")
    
    return email_subscribers, sms_subscribers


def email_alert (to, subject, body): # most important: for sending the email
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user, password = "kairosweather@gmail.com", KAIROSWEATHER_GMAIL_API_KEY # github secret
    msg['from'] = user
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
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

    email_subscribers, sms_subscribers = subscribers()
    for data in email_subscribers:
        email_alert(data[0], f"What's the Weather Right Now? ({today()})", script(data[1], data[2], "email"))
        print("    " + "- sent to:", data[0], "in", data[2])
    for data in sms_subscribers:
        email_alert(data[0], f"Weather Update ({today()})", script(data[1], data[2], "sms"))
        print("    " + "- sent to:", data[0].split("@")[0], "in", data[2])

    print(f"\nSuccess: {today()}\n")


def run(): # schedule the email to send every day at a specific time
    print("\nKairos initiated...\n")
    schedule.every().day.at("09:00").do(send)
    while True:
        print("    " + "- checking in:", datetime.now().time())
        schedule.run_pending()
        # send() # uncomment to send immediately for testing purposes
        time.sleep(1500)


run()
