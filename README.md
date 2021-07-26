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
- Press Enter in the Terminal, and Kairos will run
- When Prompted in the Terminal, manually schedule when the emails should send 
  - To send emails immediately for testing, uncomment the send() line in the run() function in main.py

## Prerequisites:
Additional modules required (these modules will be imported automatically, so don't worry):
- pyowm
- schedule

Before using Kairos, you must complete these two steps:
- Create OpenWeatherMap API Key - https://OpenWeatherMap.com/API 
- Create Google App Password - https://myaccount.google.com/security
    - Turn on 2-Step Verification
    - Create 'App Password'

Then, you must type this information in:
- assets/personal/openweathermap_api_key.txt
- assets/personal/gmail_app_password.txt

You must also type your Gmail address in:
- assets/personal/gmail_username.txt

## Storing Subscriber Data:

In the current stage of development, data management in Kairos is unfortunately done by manually editing text files.

The subscriber data used by Kairos is:
- Email
- Name
- Location

These three things should be separated by ' & '.
###### Example: email@address.com & First Name & Location

You should store this information in:
- assets/subscribers/email.txt
- assets/subscribers/sms.txt
###### Note: For SMS, you need to use an [Email-to-SMS address](https://avtech.com/articles/138/list-of-email-to-sms-addresses/).

In the text files, there is a line with the text:
- UNSUBSCRIBED:

Underneath this text, you can store the data of subscribers who have unsubscribed (or, you could delete the information).

## Guide for Location:
The location must be compatible with OpenWeatherMap's search engine - https://openweathermap.org/.

Make sure to test that:
- Your location works.
- The location fetched is the actual location you want.
  - Good Example: Seongnam-si, Korea  ->  note that this location requires a dash('-').
  - Good Example: Dallas, US  ->  Kairos uses 'US' to perform United States-specific actions like using Farenheit.
  - Bad Example: Middletown, US  ->  since there are multiple cities in the US with that name, the location fetched may not be correct.


That's it! When these prerequisites are fulfilled, you should now be able to run Kairos in your Terminal.

If running Kairos in an IDE's Terminal, make sure to open the general folder, and not just main.py, as Kairos needs to reach the 'assets' folder.

Kairos is continuously being improved. If an error occurs, please create an issue (or even help out!).

