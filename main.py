
from urllib.request import Request, urlopen
import json

class weather_json:

    def __init__(self):
        print("")

    #method for forming the request
    def form_req(self,pin):
        req = Request('http://wttr.in/%s?format=j1'%pin)
        return req

    #method for getting json response
    def get_json(self,req):
        response = urlopen(req)
        response_json = json.loads(response.read())
        return response_json

    # method for converting Fahrenheit into Celcius
    def convert_FtoC(self, temperature_F):
        temperature_C = (5 / 9) * (float(temperature_F) - 32.0)
        return round(temperature_C,1)

    #parsing json for current weather conditions
    def get_curr_details(self,response_json):

        curr_response = (response_json["current_condition"])[0]  #list under current condition key
        curr_temp_F = curr_response["temp_F"]   #current temperature
        feels_like_temp_F = curr_response["FeelsLikeF"] #feels like temperature
        description = curr_response["weatherDesc"][0]['value']  #weather description
        curr_temp_C = self.convert_FtoC(curr_temp_F)  #converting current temperature in F to C
        feels_like_temp_C = self.convert_FtoC(feels_like_temp_F) #converting feels like temperature in F to C

        #print statements for user
        print("Current Weather Conditions\n")
        print("Current Temperature in Fahrenheit: ",curr_temp_F)
        print("Current Temperature in Celcius: ", curr_temp_C)
        print("Feels Like Temperature in Fahrenheit: ", feels_like_temp_F)
        print("Feels Like Temperature in Celcius: ", feels_like_temp_C)
        print("Weather Description: ", description)
        print("\n")

    # parsing json for weather forecast for a number of hours and displaying the result
    def get_forecast(self,response_json,num_hours):
        temperature = [0.0] * num_hours   #list for storing temperatures for the next num_hours
        feels_like_temp = [0.0] * num_hours #list for storing feel like temperatures for the next num_hours
        description = [""] * num_hours #list for storing weather description for the next num_hours

        curr_response = (response_json["weather"])[0]  #list under the weather key
        hourly_response = curr_response["hourly"] #list under the hourly key

        for i,element in enumerate(hourly_response):
            #parsing current temperatures, feel like temperatures and descriptions
            if i < num_hours:
                temperature[i] = element["tempF"]
                feels_like_temp[i] = element["FeelsLikeF"]
                description[i] = element["weatherDesc"][0]["value"]

        # print statements for user
        print("Weather Forecast for the next three hours\n")

        for i in range(0,num_hours):
            print("Hour %s"%(i+1))
            print("Current Temperature in Fahrenheit: ",temperature[i])
            print("Feels Like Temperature in Fahrenheit: ", feels_like_temp[i])
            print("Weather Description: ", description[i])
            print("\n")


if __name__ == '__main__':

    #prompting the user to enter a zip code and checking the input sanity
    while True:
        try:
            zip_code = int(input("Please enter a 5 Digit US ZIP CODE: "))
        except ValueError:
            print("ERROR: This value is not allowed. Please try again.")
            continue
        else:
            if zip_code < 1 or zip_code > 99999:
                print("ERROR: This value is not allowed. Please try again.")
                continue
            elif len(str(zip_code)) != 5:
                print("ERROR: This value is not allowed. Please try again.")
                continue
            else:
                break

    weather = weather_json()
    req = weather.form_req(zip_code)
    response = weather.get_json(req)
    weather.get_curr_details(response)

    #prompting the user if they want the future forecast as well
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
                weather.get_forecast(response,3)
                break

