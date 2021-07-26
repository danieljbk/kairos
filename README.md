<img src="https://user-images.githubusercontent.com/79312811/126855101-e5f8f078-1154-46b3-bc7b-ad2066735e64.png" width="200" height="200">

# Kairos the Weather Bot
Kairos is a script that periodically sends weather information through email or text.
###### Note: It should be run on an interface that can accept inputs (for scheduling the email).

## How to Run Kairos:
- Download kairos-main
- Complete prerequisites (described below)
- Complete subscriber data setup
- Open Terminal
- Type 'python ' into the Terminal (don't forget the space)
- Drag the main.py file into the Terminal (this will paste the filepath into the Terminal)
- Press Enter in the Terminal
- Kairos will run
- In the Terminal, schedule when the emails should send
- (To send emails immediately for testing, uncomment the send() line in the run() function in main.py)

## Prerequisites:
Additional modules required (these modules will be imported automatically, so don't worry):
- pyowm
- schedule

Before using Kairos, you must complete these two steps:
- Create OpenWeatherMap API Key - https://OpenWeatherMap.com/API 
- Create Google App Password - https://myaccount.google.com/security
    - Turn on 2-Step Verification
    - Create 'App Password'

When these prerequisites are fulfilled, you should download Kairos.

Then, you must type this information in:
- assets/personal/openweathermap_api_key.txt
- assets/personal/gmail_app_password.txt

You must also type your Gmail address in:
- assets/personal/gmail_username.txt
 
That's it! You should now be able to run Kairos in your IDE or Terminal.

Make sure you open the general folder, and not just main.py, as it has to be able to reach the assets folder.

If an error occurs, please notify me by creating an issue. Thank you!

## Reading Subscriber Data:
The subscriber data used by Kairos is:
- Email
- Name
- Location

###### Note: These three things must be separated by ' & '.
###### Example: email@address.com & First Name & Location

To use Kairos, you must create:
- Text file containing your subscriber data called email.txt
- Text file containing your subscriber data called sms.txt

Then, you must store this information in:
- assets/subscribers/email.txt
- assets/subscribers/sms.txt

In the text files, there must be a line with the text:
- UNSUBSCRIBED:

Underneath this text, you can store the data of subscribers who have unsubscribed (or, you could delete the information).

Currently, any edits to these files must be made manually.

## Guide for Location:
The location must be compatible with OpenWeatherMap's search engine - https://openweathermap.org/.

Test that:
- Your location works.
- The location fetched is the actual location you want.

###### Good Example: Seongnam-si, Korea  # This location requires a dash('-').
###### Good Example: Dallas, US  # Kairos uses 'US' to perform United States-specific actions like using Farenheit.
###### Bad Example: Middletown, US  # since there are multiple cities in the US with that name, the location fetched may not be correct.

