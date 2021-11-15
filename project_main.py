import pandas as pd
from secrets import API_user_email  # email for generating your own API key
from secrets import API_user_key    # must generate API key using your own email

from requests import request
import json
from pandas.io.json import json_normalize

print(API_user_email, API_user_key)
"""
New York:
      "code": "001","value_represented": "Albany"   "code": "003","value_represented": "Allegany" (001 to 123)
====
      "code": "061","value_represented": "New York" "code": "081","value_represented": "Queens"
      "code": "085","value_represented": "Richmond" "code": "047","value_represented": "Kings" 
      "code": "005","value_represented": "Bronx"
Main Documentation:
https://aqs.epa.gov/aqsweb/documents/data_api.html#meta
"""
"https://aqs.epa.gov/data/api/list/parametersByClass?email=Hilarion.Reyes12@myhunter.cuny.edu&key=amberram68&pc=ALL"
"https://aqs.epa.gov/data/api/sampleData/byState?email=test@aqs.api&key=test&param=45201&bdate=19950515&edate=19950515&state=37"
"https://aqs.epa.gov/data/api/list/parametersByClass?email=test@aqs.api&key=test&pc=ALL"
sample_query = "(   https://aqs.epa.gov/data/api/sampleData/byState?email=Hilarion.Reyes12@myhunter.cuny.edu&key=amberram68&param=45201&bdate=19950515&edate=19950515&state=37  )"
#with open()
response = request(
    url = "https://aqs.epa.gov/data/api/sampleData/byState?email=test@aqs.api&key=test&param=45201&bdate=19950515&edate=19950515&state=37", 
    method='get')

data = response.json()
data = json.loads(data)
json_normalize(data['results'])

#data = pd.read_json("https://aqs.epa.gov/data/api/sampleData/byState?email=test@aqs.api&key=test&param=45201&bdate=19950515&edate=19950515&state=37")
print(data)
# must change -> param, bdate, edate, state, county
query1 = 0
pollute_param = {   "42102": "Carbon dioxide", "43201": "Methane", "42401": "Sulfur dioxide", 
                    "42603": "Oxides of nitrogen(NOx)", "42101": "Carbon monoxide"
                }

#API Key =
#
#pd.read_json()
