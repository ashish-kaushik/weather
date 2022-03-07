# Weather Script


A short Python script that runs in the terminal and does the following. Everything is done with the Python standard library. However, used the requests library as well. No external libraries are used except requests.

The script does the following:

1. Prompts the user for their US Post Office ZIP code.
2. Using the weather service at wttr.in, gets their weather report as a JSON file. Documentation for this service at http://wttr.in/:help. As well as https://github.com/chubin/wttr.in 
3. Clearly shows the user the current temperature and the ‘feels like’ temperature in Fahrenheit, as well as the description of the current weather.
4. Converts the temperature given to you in Fahrenheit to Celsius, and shows that converted value to the user. 
5. The conversion is accurate to the first decimal place, rounded appropriately. For example, if it’s zero degrees F, the script will show the user -17.8 C.
6. Shows the user an emoji based on what range the temperature in Celsius falls into.
7. Shows the weather forecast for the next three hours, includes the same data points as the current conditions: Temperature, ‘feels like’, weather description. 
