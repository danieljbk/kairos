# Kairos the Weather Bot
Automated Weather Information Emailing System

## Before using Kairos, you must create:
- OpenWeatherMap API Key - https://OpenWeatherMap.com/API 
- Google App Password - https://myaccount.google.com/security
    - Turn on 2-Step Verification
    - Create 'App Password'

## Reading Subscriber Data:
To use Kairos, you must create text files containing your subscriber data called email.txt and sms.txt.

The location of the files must be in assets/subscribers/*.txt.

The subscriber data used by Kairos is:
- Email
- Name
- Location

###### Note: These three things must be separated by ' & '.
###### Example: email@address.com & First Name & Location

## Guide for Location:
The location must be compatible with OpenWeatherMap's search engine - https://openweathermap.org/.

Test that your location works, and that the location fetched is the actual location you want.

###### Good Examples: Dallas, US or Seongnam-si, Korea
###### Bad Example: Middletown, US # since there are multiple cities in the US called Middletown, the location fetched will likely not be the Middletown you want.

###### Note: Kairos uses 'US' to perform United States-specific actions like using Farenheit.
