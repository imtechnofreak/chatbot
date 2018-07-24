import sys
sys.path.append('/home/olivier/workspace/python-aiml')
import aiml
# The Kernel object is the public interface to
# the AIML interpreter.
k = aiml.Kernel()

# Use the 'learn' method to load the contents
# of an AIML file into the Kernel.
k.learn("std-startup.xml")

# Use the 'respond' method to compute the response
# to a user's input string.  respond() returns
# the interpreter's response, which in this case
# we ignore.
k.respond("load aiml b")

def processRequest(req):
    print("AIML")
    query = req.get("result").get("resolvedQuery")
    res = k.respond(query)
    print(res)

    return res