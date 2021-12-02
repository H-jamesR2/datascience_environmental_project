import urllib.request
import pandas as pd
from secrets import API_user_email  # email for generating your own API key
from secrets import API_user_key    # must generate API key using your own email

import requests
import json
from pandas.io.json import json_normalize

print(API_user_email, API_user_key)
"""
# Code = 36
New York:
      "code": "001","value_represented": "Albany"   "code": "003","value_represented": "Allegany" (001 to 123)
====
      "code": "061","value_represented": "New York" "code": "081","value_represented": "Queens"
      "code": "085","value_represented": "Richmond" "code": "047","value_represented": "Kings" 
      "code": "005","value_represented": "Bronx"
      # New York County just missing...
      
main target sample:
      "units_of_measure": "Parts per billion Carbon",
      "units_of_measure_code": "078",
      "sample_duration": "24 HOUR",
      "sample_duration_code": "7",
      "sample_frequency": "EVERY 6TH DAY",
      "detection_limit": 0.042,
Main Documentation:
https://aqs.epa.gov/aqsweb/documents/data_api.html#meta

Sources:
get data:   https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
read data:  https://stackoverflow.com/questions/1871524/how-can-i-convert-json-to-csv/58648286#58648286
convert list of dictionaries to dataframe:      
      https://stackoverflow.com/questions/20638006/convert-list-of-dictionaries-to-a-pandas-dataframe
"""
#get elements
"https://aqs.epa.gov/data/api/list/parametersByClass?email=Hilarion.Reyes12@myhunter.cuny.edu&key=amberram68&pc=ALL"

"https://aqs.epa.gov/data/api/sampleData/byState?email=test@aqs.api&key=test&param=45201&bdate=19950515&edate=19950515&state=37"
"https://aqs.epa.gov/data/api/list/parametersByClass?email=test@aqs.api&key=test&pc=ALL"
sample_query = "(   https://aqs.epa.gov/data/api/sampleData/byState?email=Hilarion.Reyes12@myhunter.cuny.edu&key=amberram68&param=45201&bdate=19950515&edate=19950515&state=36  )"

target_query_2019 = "(   https://aqs.epa.gov/data/api/sampleData/byState?email=Hilarion.Reyes12@myhunter.cuny.edu&key=amberram68&param=45201&bdate=20190501&edate=20191231&state=36  )"

target_query_2020 = "(   https://aqs.epa.gov/data/api/sampleData/byState?email=Hilarion.Reyes12@myhunter.cuny.edu&key=amberram68&param=45201&bdate=20200101&edate=20201231&state=36  )"
target_query_2021 = "(   https://aqs.epa.gov/data/api/sampleData/byState?email=Hilarion.Reyes12@myhunter.cuny.edu&key=amberram68&param=45201&bdate=20210101&edate=20210501&state=36  )"

target_query_NY = "(   https://aqs.epa.gov/data/api/sampleData/byCounty?email=Hilarion.Reyes12@myhunter.cuny.edu&key=amberram68&param=45201&bdate=20200101&edate=20201231&state=36&county=061  )"

#296 rows
with urllib.request.urlopen("https://aqs.epa.gov/data/api/sampleData/byState?email=Hilarion.Reyes12@myhunter.cuny.edu&key=amberram68&param=45201&bdate=20210101&edate=20210501&state=36") as url:
    data = json.loads(url.read().decode())
    #print(data)

#create dataframe -> buildts two columns (Header and Data)
#containing list of dictionary
df = pd.json_normalize(data)
print(df)

for value in df['Data']:
      print(type(value[0]))
      print(len(value))
      main_df = pd.DataFrame(value)
print(main_df)
#r = requests.get("https://aqs.epa.gov/data/api/sampleData/byState?email=Hilarion.Reyes12@myhunter.cuny.edu&key=amberram68&param=45201&bdate=20210101&edate=20210501&state=36")
# if response type was set to JSON, then you'll automatically have a JSON response here...
#print(r.json())

#with open()
"""
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
"""
