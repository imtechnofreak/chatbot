def process_request(req):
    """ Processes a greeting intent """
    if req.get("result").get("action") != "greetings.start":
        return {}
    
    original_request = req.get("originalRequest")
    uid = ''
    user_query = None
    if original_request:
        uid = original_request.get("data").get("user").get("userId")

    res = make_result_data(user_query)
    return res

def make_result_data(query):
    """ returns the user's"""
    if not query:
       parameters = {
           "firstName": "Olivier"
       }
       return parameters

    parameters = {
        "firstName": query.first_name
    }
    return parameters