import datetime
import urllib3

#global since everyone accesses it
URL_TO_MONITOR = "www.skipq.org"
    
def lambda_handler(event, context):
    values = dict()
    avail = get_availability()
    latency = get_latency()
    values.update({
        "availability": avail,
        "latency": latency
    })
    return values
    
    
def get_availability():
    ### Returns 1.0 if available and 0 if not
    http = urllib3.PoolManager()
    response = http.request("GET", URL_TO_MONITOR)
    if response.status == 200:
        return 1.0
    else:
        return 0.0


def get_latency():
    ### Returns latency in seconds
    http = urllib3.PoolManager()
    start = datetime.datetime.now()
    response = http.request("GET", URL_TO_MONITOR)
    end = datetime.datetime.now()
    delta = end - start
    latencySec = round(delta.microseconds * .000001, 6)
    return latencySec
    
    
   