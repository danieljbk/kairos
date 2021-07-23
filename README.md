# kairos
Automated Weather Information Emailing System

## Before using Kairos, you must create:
1. OpenWeatherMap API Key - OpenWeatherMap.com/API
2. Google App Password - https://myaccount.google.com/security
    a. Turn on 2-Step Verification
    b. Create 'App Password'

## Reading Subscriber Data:
To use Kairos, you must create a text file containing your subscriber data.

They must be called email.txt and sms.txt.

The location of the files must be in assets/subscribers/*.txt.

The subscriber data used in Kairos is:
1. Email
2. Name
3. Location

###### Note: These three things must be separated by ' & '.
###### example: email@address.com & First Name & Location

## Location
Guide for Location:
The location must be compatible with OpenWeatherMap's search engine - https://openweathermap.org/.

Test that your location works, and that the location fetched is the actual location you want.

Good Examples: 
1. Dallas, US
2. Seongnam-si, Korea

Bad Example:
1. Middletown, US # since there are multiple cities in the US called Middletown, the location fetched may not be the Middletown you want.

###### Note: Kairos uses 'US' to perform United States-specific actions like using Farenheit.
