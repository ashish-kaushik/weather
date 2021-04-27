# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from urllib.request import Request, urlopen
import re

class weather:
    def __init__(self):
         print('hi')

    #method of forming the request
    def form_req(self,pin):
        req = Request('http://wttr.in/%s?0'%pin)
        return req

    #method for getting html response
    def get_html(self,req):
        response = urlopen(req)
        response_bytes = response.read()
        response_html = response_bytes.decode('utf-8')
        return response_html

    def get_details(self,response_html):

        curr_key_identify = "^Weather.*"   #current weather key identifier
        curr_pattern = "</span>.*"
        description = ""
        curr_temp = None
        feels_like_temp = None
        index = 0  # index declaration for the current weather

        html_list = response_html.split("\n")  #converting html response into a list

        #finding the index of the line where Weather report starts
        for i,line in enumerate(html_list):
            results = re.search(curr_key_identify, line)
            if results != None:
                index = i
                break

        ### FINDING WEATHER DESCRIPTION ###
        # checking the presence of </span> tag in "Weather Description" line
        results= re.search(curr_pattern,html_list[index+2])

        if results == None:
            description = html_list[index+2].strip(" ")  #only the description is present as there's no </span> tag
        else:
            obj = results.group()
            description = re.sub("<.*?>", "", obj)  #</span> is present so scraping Description accordingly
            description = description.strip()

        ### FINDING CURREENT TEMPERATURE AND FEELS LIKE TEMPERATURE ###
        curr_pattern = r"<span.*>.*</span> <span.*>.*</span>.*"
        curr_pattern_results = re.search(curr_pattern, html_list[index+3])  # searching pattern in line consisting o
        curr_pattern_results = curr_pattern_results.group()  # grouping the search results
        curr_pattern_results = re.sub("<.*?>", "", curr_pattern_results)  # removing HTML tags
        curr_pattern_results = re.findall(r'\d+', curr_pattern_results)  # getting all the numbers
        if len(curr_pattern_results) > 1:   #cheking if feels like temperature is there
            curr_temp = curr_pattern_results[0]
            feels_like_temp = curr_pattern_results[1]
        else:
            curr_temp = curr_pattern_results[0]

        return(description,curr_temp,feels_like_temp)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # us_pin = input()
    # weather = weather(us_pin)

    weather = weather()
    req = weather.form_req('15217')
    response = weather.get_html(req)
    description, curr_temp, feels_like_temp = weather.get_details(response)
    print(description, curr_temp, feels_like_temp)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
