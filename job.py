"""
Example script cleaning up given Settings 2.0 namespaces after a configurable period of time.
"""
import requests, datetime
from datetime import datetime
import os
import http.server
# the number of days a setting entry is kept until its deleted and cleaned up again
KEEP_PERIOD_DAYS = int(os.environ.get('KEEP_PERIOD_DAYS', '14'))

YOUR_DT_API_URL = os.environ.get('DYNATRACE_ENVIRONMENT_URL')
YOUR_DT_API_TOKEN = os.environ.get('DYNATRACE_API_TOKEN') # Dynatrace API token with v2 settings read and write scope activated
# A list of namespaces that should be automatically cleaned
NS_STR = os.environ.get('SETTINGS_SCHEMAS')
# Split the comma separated string into a list
NAMESPACES = NS_STR.split(',') if NS_STR else []

def check(items):
    now = datetime.now().timestamp()
    for item in items:
        if item['modified'] / 1000 < now - (86400 * KEEP_PERIOD_DAYS): # item older than X days, delete it
            dr = requests.delete(YOUR_DT_API_URL + '/api/v2/settings/objects/' + item['objectId'], headers={'Authorization' : 'Api-Token ' + YOUR_DT_API_TOKEN})
            if dr.status_code == 204:
                print("Successfully removed settings object with id: %s" % (item['objectId']))
        
def cleanup():
    if not YOUR_DT_API_URL or not YOUR_DT_API_TOKEN or not NAMESPACES:
        print("Please set the necessary environment variables: KEEP_PERIOD_DAYS, DYNATRACE_API_TOKEN, DYNATRACE_ENVIRONMENT_URL, SETTINGS_SCHEMAS")
        exit(1)
    for ns in NAMESPACES:
        print("Start cleaning up namespace: %s" % (ns))
        count = 0
        r = requests.get(YOUR_DT_API_URL + '/api/v2/settings/objects?fields=objectId,modified&schemaIds=' + ns, headers={'Authorization' : 'Api-Token ' + YOUR_DT_API_TOKEN})
        if r.status_code == 200: 
            count = count + len(r.json()['items'])
            check(r.json()['items'])  
            while count < r.json()['totalCount']:
                r = requests.get(YOUR_DT_API_URL + '/api/v2/settings/objects?nextPageKey=' + r.json()['nextPageKey'], headers={'Authorization' : 'Api-Token ' + YOUR_DT_API_TOKEN})
                if r.status_code == 200: 
                    count = count + len(r.json()['items'])
                    check(r.json()['items'])
                else:
                    print("Http error: %d" % (r.status_code))
                    break
        else:
            print("Http error: %d" % (r.status_code))

cleanup()
        



