
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from datetime import datetime, timedelta
import json
import sys



class weather:

    def __init__(self):
        print("")

    def get_emoji(self, temperature):
        temperature = self.convert_FtoC(temperature)
        if temperature <= 10:
            chilly_face = '\U0001F976'
            return chilly_face
        elif 10 < temperature <= 20:
            facesmiling = '\U0001F600'
            return facesmiling
        elif 20 < temperature <= 30:
            heart_eyes = '\U0001F60D'
            return heart_eyes
        elif temperature > 30:
            hot_face = '\U0001F975'
            return hot_face

    # method for forming the request
    def form_req(self, pin):
        req = Request('http://wttr.in/:%s?format=j1'%pin)
        return req

    # method for getting json response
    def get_json(self, req):

        try:
            response = urlopen(req)
        except HTTPError as error:
            if error.code == 404:
                return None

        response_json = json.loads(response.read())
        return response_json

    # method for converting Fahrenheit into Celcius
    def convert_FtoC(self, temperature_F):
        temperature_C = (5 / 9) * (float(temperature_F) - 32.0)
        return round(temperature_C, 1)

    # parsing json for current weather conditions
    def get_curr_details(self, response_json):
        curr_response = (response_json["current_condition"])[0]  # list under current condition key
        curr_temp_F = float(curr_response["temp_F"])  # current temperature
        feels_like_temp_F = float(curr_response["FeelsLikeF"])  # feels like temperature
        description = curr_response["weatherDesc"][0]['value']  # weather description
        curr_temp_C = self.convert_FtoC(curr_temp_F)  # converting current temperature in F to C
        feels_like_temp_C = self.convert_FtoC(feels_like_temp_F)  # converting feels like temperature in F to C

        # print statements for user
        print("Current Weather Conditions\n")
        print("Current Temperature in Fahrenheit: ", curr_temp_F, self.get_emoji(curr_temp_F))
        print("Current Temperature in Celcius: ", curr_temp_C, self.get_emoji(curr_temp_F))
        print("Feels Like Temperature in Fahrenheit: ", feels_like_temp_F, self.get_emoji(feels_like_temp_F))
        print("Feels Like Temperature in Celcius: ", feels_like_temp_C, self.get_emoji(feels_like_temp_F))
        print("Weather Description: ", description)
        print("\n")

    def get_format_date_time(self, curr_date_time, num_hours):
        next_hours = [""] * num_hours
        next_hours_date = [""] * num_hours
        next_hours_time = [0] * num_hours
        for n in range(0, num_hours):
            next_hours[n] = curr_date_time + timedelta(hours=n+1)   # next n hour
            next_hours_date[n] = next_hours[n].date()   # next n hour date
            next_hours_time[n] = str(next_hours[n].time())[:5]   # next n hour time
            next_hours_time[n] = int(next_hours_time[n].replace(":", ""))  # formatting hh:mm to hhmm

        return (next_hours_date, next_hours_time)

    def get_details(self, curr_date_time, next_hours_date, next_hours_time, num_hours, response_json):
        curr_date = curr_date_time.date()

        temperature = [0.0] * num_hours  # list for storing temperatures for the next num_hours
        feels_like_temp = [0.0] * num_hours  # list for storing feel like temperatures for the next num_hours
        description = [""] * num_hours  # list for storing weather description for the next num_hours

        for n in range(0, num_hours):
            if next_hours_date[n] == curr_date:
                curr_response = (response_json["weather"])[0]  # list under the weather key for the same day
            else:
                curr_response = (response_json["weather"])[1]  # list under the weather key for the next day
            index = int( next_hours_time[n] / 300)  # index of the n hour to get the hour from "hourly" key
            hourly_response = curr_response["hourly"][index]  # list under the hourly key
            temperature[n] = float(hourly_response["tempF"])
            feels_like_temp[n] = float(hourly_response["FeelsLikeF"])
            description[n] = hourly_response["weatherDesc"][0]["value"]

        return (temperature, feels_like_temp, description)



    # parsing json for weather forecast for a number of hours and displaying the result
    def get_forecast(self, response_json, num_hours):
        curr_date_time = datetime.now()       # current time and date
        curr_date = curr_date_time.date()     # current date

        next_hours_date, next_hours_time = self.get_format_date_time(curr_date_time, num_hours)

        temperature, feels_like_temp, description = self.get_details(curr_date_time, next_hours_date, next_hours_time, num_hours, response_json)

        # print statements for user
        print("Weather Forecast for the next three hours\n")

        for i in range(0, num_hours):
            print("Time ", (str(next_hours_time[i])[:2] + ":" + str(next_hours_time[i])[2:]))
            print("Temperature in Fahrenheit: ", temperature[i], self.get_emoji(temperature[i]))
            print("Feels Like Temperature in Fahrenheit: ", feels_like_temp[i], self.get_emoji(feels_like_temp[i]))
            print("Weather Description: ", description[i])
            print("\n")
    # method to check if the zip belongs to the US
    def is_zip_us(self, response_json):
        curr_response = (response_json["nearest_area"])[0]  # list under nearest area key
        country = (curr_response["country"][0])["value"]
        if country == "United States of America":
            return True
        else:
            return False




if __name__ == '__main__':

    num_hours = 3
    first_time = True
    weather = weather()
    response = ""
    Timeout = 30

    while True:
        # prompting the user if they want to check weather for another zip code
        while True and not first_time:
            try:
                continue_response = str.lower(input("Would you like to check weather for another zip code: "))
            except ValueError:
                print("ERROR: This value is not allowed. Please try again. Enter the word YES or NO.")
                continue
            else:
                if continue_response != "yes" and continue_response != "no":
                    print("ERROR: This value is not allowed. Please try again. Enter the word YES or NO.")
                    continue
                elif continue_response == "no":
                    print("Thank you for using this application.")
                    sys.exit()
                elif continue_response == "yes":
                    break


        while True:
            # prompting the user to enter the zip code
            try:
                zip_code = int(input("Please enter a 5 Digit US ZIP CODE: "))
            except ValueError:
                print("ERROR: This value is not allowed. Please enter a valid 5 Digit US ZIP CODE.")
                continue
            else:
                if zip_code < 1 or zip_code > 99999:
                    print("ERROR: This value is not allowed. Please enter a valid 5 Digit US ZIP CODE.")
                    continue
                elif len(str(zip_code)) != 5:
                    print("ERROR: This value is not allowed. Please enter a valid 5 Digit US ZIP CODE.")
                    continue
                else:
                    req = weather.form_req(zip_code)
                    response = weather.get_json(req)
                    if response == None:    # checking if the zip exists
                        print("ERROR: zip located in Mars. Please enter a zip on Earth.")
                        continue
                    elif not weather.is_zip_us(response):  # checking if the zip is in US
                        print("ERROR: This zip is not in US. Please enter a valid 5 Digit US ZIP CODE.")
                        continue
                    else:
                        break


        weather.get_curr_details(response)  # current weather conditions
        first_time = False

        # prompting the user if they want the future forecast as well
        while True:
            try:
                help_response = str.lower(input("Would you also like to see the next 3 hours forecast? (Enter YES or NO): "))
            except ValueError:
                print("ERROR: This value is not allowed. Please try again. Enter the word YES or NO.")
                continue
            else:
                if help_response != "yes" and help_response != "no":
                    print("ERROR: This value is not allowed. Please try again. Enter the word YES or NO.")
                    continue
                elif help_response == "no":
                    break
                elif help_response == "yes":
                    weather.get_forecast(response, num_hours)
                    break

