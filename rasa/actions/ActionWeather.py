from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from rasa_core.actions import Action
from rasa_core.events import SlotSet

import json


class WeatherAPI:
    def process_request(self, req):
        """ Processes a weather intent query """
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = self.make_yql_query(req)
        if yql_query is None:
            return {}
        yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
        result = urlopen(yql_url).read().decode('utf-8')
        data = json.loads(result)
        # res = makeResultString(data)
        res = self.make_result_data(data)
        return res

    def make_yql_query(self, req):
        """ Queries the yahoo weather API for a given city """
        city = req.get("city")
        if not city:
            city = "waterloo"
        return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "') and u='c'"

    def make_result_data(self, data):
        """ Returns a dictionary with the data """
        query = data.get('query')
        if query is None:
            return {}

        result = query.get('results')
        if result is None:
            return {}

        channel = result.get('channel')
        if channel is None:
            return {}

        item = channel.get('item')
        location = channel.get('location')
        units = channel.get('units')
        if (location is None) or (item is None) or (units is None):
            return {}

        condition = item.get('condition')
        if condition is None:
            return {}

        parameters = {
            "city" : location.get("city"),
            "description": condition.get("text"),
            "temperature": condition.get("temp"),
            "unit": units.get("temperature")
        }
        
        return parameters

class ActionWeather(Action):
    def name(self):
        return 'action_weather'

    def run(self, dispatcher, tracker, domain):
        weatherApi = WeatherAPI()
        city = tracker.get_slot('city')
        if city is None:
            city = "Waterloo"

        weather_dict = weatherApi.process_request({"city": city})
        dispatcher.utter_message("Weather action!")
        return [SlotSet("city", weather_dict['city'] if weather_dict['city'] is not None else []),
                SlotSet("temperature", weather_dict['temperature'] if weather_dict['temperature'] is not None else [])]