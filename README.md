# Kairos the Weather Bot
Kairos is a script that periodically sends weather information through email or text.
###### Note: It should be run on an interface that can accept inputs (for scheduling the email).

## Prerequisites:
Before using Kairos, you must create:
- OpenWeatherMap API Key - https://OpenWeatherMap.com/API 
- Google App Password - https://myaccount.google.com/security
    - Turn on 2-Step Verification
    - Create 'App Password'

When these prerequisites are fulfilled, you should download Kairos.

Then, you must type this information in:
- assets/private/openweathermap_api_key.txt
- assets/private/gmail_app_password.txt

You must also type your email address in:
- assets/private/gmail_username.txt
 
That's it!

You should now be able to run Kairos in your terminal.

If there is an error, please create an issue. Thanks!

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

