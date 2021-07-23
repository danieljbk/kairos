# kairos
Automated Weather Information Emailing System


Reading Subscriber Data:
To use Kairos, you must create a text file containing your subscriber data.
They must be called email.txt and sms.txt.
The location of the files must be in assets/subscribers/*.txt.

The subscriber data used in Kairos is:
1. Email
2. Name
3. Location

These three things must be separated by ' & '.
example: email@address.com & First Name & Location

Guide for Location:
The location must be compatible with OpenWeatherMap's search engine - https://openweathermap.org/.
Test that your location works, and that the location fetched is the actual location you want.
example: Dallas, US
example: Seongnam-si, Korea

Note: Kairos uses 'US' to perform United States-specific actions like using Farenheit.
