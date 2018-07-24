import json

def process_request(req):
    """ Processes a weather intent query """
    if req.get("result").get("action") != "weather.start":
        return {}
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = make_yql_query(req)
    if yql_query is None:
        return {}
    yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    result = urlopen(yql_url).read().decode('utf-8')
    data = json.loads(result)
    # res = makeResultString(data)
    res = make_result_data(data)
    return res


def make_yql_query(req):
    """ Queries the yahoo weather API for a given city """
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if not city:
        city = "waterloo"
    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "') and u='c'"

def make_result_string(data):
    """ Forms the response string to send to the user """
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

    # print(json.dumps(item, indent=4))

    speech = "Today the weather in " + location.get('city') + ": " + condition.get('text') + \
             ", And the temperature is " + condition.get('temp') + " " + units.get('temperature')
    
    return speech

def make_result_data(data):
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
