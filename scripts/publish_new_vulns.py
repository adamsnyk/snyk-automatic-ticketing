import os
import json
import requests

from pprint import pprint
from datetime import date, timedelta

yesterday = str(date.today() - timedelta(1))
today = str(date.today())

# Params for the 10 latest issues
LIMIT = 25
URL = 'https://snyk.io/api/v1/reporting/issues/?from={}&to={}&sortBy=introducedDate&order=desc&page=1&perPage={}'.format(yesterday, today, LIMIT)
HEADERS = {"Authorization": "Token {}".format(os.environ["SNYK_TOKEN"])}
DATA = {
  "filters": {
    "orgs": [os.environ["SNYK_ORG"]],
    "types": [
      "vuln",
      "license",
      "configuration"
    ]
  }
}

# Get Latest Issues as dict
r = requests.post(
    URL,
    headers=HEADERS,
    json=DATA,
)
json_response = json.loads(r.content)

# Filter for yesterday's results
yesterday_results = []
for result in json_response['results']:
    if yesterday <= result['introducedDate'] and result['introducedDate'] < today:
        yesterday_results.append(result)

# Send to your ticketing system
for result in yesterday_results:
    # TODO: API Post call int your ticketing system
    pprint(result)
