# Kairos the Weather Bot
Automated Weather Information Emailing System

## Prerequisites:
Before using Kairos, you must create:
- OpenWeatherMap API Key - https://OpenWeatherMap.com/API 
- Google App Password - https://myaccount.google.com/security
    - Turn on 2-Step Verification
    - Create 'App Password'

Then, you must store this information in:
- assets/private/secret.txt
 
## Reading Subscriber Data:
To use Kairos, you must create:
- Text file containing your subscriber data called email.txt
- Text file containing your subscriber data called sms.txt

Then, you must store this information in:
- assets/subscribers/email.txt
- assets/subscribers/sms.txt

In the text files, there must be a line with the text 'UNSUBSCRIBED:'.
Underneath this text, you can store the data of subscribers who have unsubscribed (or, you could delete the information).

Currently, any edits to these files must be made manually.

The subscriber data used by Kairos is:
- Email
- Name
- Location

###### Note: These three things must be separated by ' & '.
###### Example: email@address.com & First Name & Location

## Guide for Location:
The location must be compatible with OpenWeatherMap's search engine - https://openweathermap.org/.

Test that:
- Your location works.
- The location fetched is the actual location you want.

###### Good Example: Seongnam-si, Korea  # This location requires a dash('-').
###### Good Example: Dallas, US  # Kairos uses 'US' to perform United States-specific actions like using Farenheit.
###### Bad Example: Middletown, US  # since there are multiple cities in the US with that name, the location fetched may not be correct.

