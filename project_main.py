"""
Title: “New York City Quarantine Analysis on Greenhouse Gas Emissions”
Resources: # Libraries (mainly used):
      urllib.request, pandas, NumPy, json, seaborn, matplotlib
URL: https://jamswhat2.github.io/datascience_environmental_project/
Github: https://github.com/Jamswhat2/datascience_environmental_project

The main data source for this project is generated through the 
aqs.epa.gov data API and is indexed at the quarterlyData, byCounty level 
generating JSON files which can be converted to csv files 
for each particular borough which we can use for analysis and visualization later on.
Typical Query used:
      https://aqs.epa.gov/data/api/quarterlyData/byCounty?email=Hilarion.Reyes12@myhunter.cuny.edu&key=amberram68&param=45201&bdate=20200101&edate=20201231&state=36&county=005
"""
# have to show because secrets.py not visible on gradescope..
API_user_email = "Hilarion.Reyes12@myhunter.cuny.edu"
API_user_key = "amberram68"
#
import urllib.request
import pandas as pd
#from secrets import API_user_email  # email for generating your own API key
#from secrets import API_user_key    # must generate API key using your own email

import numpy as np
import json

print(API_user_email, API_user_key)
"""
# File Repository: https://github.com/Jamswhat2/datascience_environmental_project
# State Code = 36
New York:
      "code": "001","value_represented": "Albany"   "code": "003","value_represented": "Allegany" (001 to 123)
====
      "code": "061","value_represented": "New York" "code": "081","value_represented": "Queens"
      "code": "085","value_represented": "Richmond" "code": "047","value_represented": "Kings" 
      "code": "005","value_represented": "Bronx"
      # New York County just missing...
      
main target sample: 
      (to record on [borough]_[parameter]_(site?)_TABLE)
      "site_number": "0110",                          #->record
      "parameter_code": "45201",
      ...
      "latitude": 40.816, "longitude": -73.902,
      ...
      "year": 2020, "quarter": "1",
      "units_of_measure": "Parts per billion Carbon",
      "event_type": "No Events",
      "observation_count": 12,                        #->record
      "observation_percent": "80.0",                  #->record
      "arithmetic_mean": 1.575,                       #->record
      "minimum_value": "0.9",                         #->record
      "maximum_value": "2.9",                         #->record
Main Documentation:
https://aqs.epa.gov/aqsweb/documents/data_api.html#meta

Sources:
get data:   https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
read data:  https://stackoverflow.com/questions/1871524/how-can-i-convert-json-to-csv/58648286#58648286
convert list of dictionaries to dataframe:      
      https://stackoverflow.com/questions/20638006/convert-list-of-dictionaries-to-a-pandas-dataframe
"""


# REFERENNCE queries:
sample_query = "(   https://aqs.epa.gov/data/api/sampleData/byState?email=Hilarion.Reyes12@myhunter.cuny.edu&key=amberram68&param=45201&bdate=19950515&edate=19950515&state=36  )"
target_query_2019 = "(   https://aqs.epa.gov/data/api/sampleData/byState?email=Hilarion.Reyes12@myhunter.cuny.edu&key=amberram68&param=45201&bdate=20190501&edate=20191231&state=36  )"
target_query_2020 = "(   https://aqs.epa.gov/data/api/sampleData/byState?email=Hilarion.Reyes12@myhunter.cuny.edu&key=amberram68&param=45201&bdate=20200101&edate=20201231&state=36  )"
target_query_2021 = "(   https://aqs.epa.gov/data/api/sampleData/byState?email=Hilarion.Reyes12@myhunter.cuny.edu&key=amberram68&param=45201&bdate=20210101&edate=20210501&state=36  )"
target_query_bronx = "(   https://aqs.epa.gov/data/api/sampleData/byCounty?email=Hilarion.Reyes12@myhunter.cuny.edu&key=amberram68&param=45201&bdate=20200101&edate=20201231&state=36&county=005  )"

# query actually implemented..
base_query = "https://aqs.epa.gov/data/api/quarterlyData/byCounty?email=" + \
    str(API_user_email)+"&key="+str(API_user_key)

# ============================================#
# combines year and quarter for generating chart x_labels.
def combine_date(year, quarter):
      return str(str(year) +'_q'+ str(quarter))

# unpacks pct_change list/series and returns pct_change array
def unpack_pct_change_list(pct_list):
      new_array = []
      for val in pct_list:
            new_array.append(val[0])
      return np.array(new_array)

# generates county/borough dataframes accounting for: 
# pollutant parameters ("codes" within array), county code, and
# the template query (standard)
def generate_county_df(template_query, pollutant_param_array, county_code):
      pollutant_queries = []

      for pollutant in pollutant_param_array:
            query_2019 = (template_query + "&param=" + str(pollutant) 
                  + "&bdate=20190401&edate=20191231&state=36" +"&county="+ str(county_code))
            query_2020 = (template_query + "&param=" + str(pollutant) 
                  + "&bdate=20200101&edate=20201231&state=36" +"&county="+ str(county_code))
            query_2021 = (template_query + "&param=" + str(pollutant) 
                  + "&bdate=20210101&edate=20210630&state=36" +"&county="+ str(county_code))
            pollutant_queries.extend([query_2019,query_2020,query_2021])
      print(len(pollutant_queries))

      output_df = pd.DataFrame()
      for query in pollutant_queries:
            print(query)
            with urllib.request.urlopen(query) as url:
                  data = json.loads(url.read().decode())
            # create dataframe -> buildts two columns from (Header and Data)
            df = pd.json_normalize(data)  # containing list of dictionary
            
            for value in df['Data']:
                  print(len(value)) # row count
                  query_df = pd.DataFrame(value)
            #print(query_df)        

            if len(query_df.columns) != 0:  # non-empty df query...
                  query_df = query_df.sort_values(
                        by=['county_code', 'pollutant_standard','quarter'])
                  query_df = query_df.loc[query_df['sample_duration'] == '1 HOUR']  #have standard duration as 1 HOUR.

                  # generate yr_quarter label for chart indexing
                  query_df['yr_quarter'] = query_df.apply(
                      lambda x: combine_date(x['year'], x['quarter']), axis=1)

                  output_df = output_df.append(query_df, ignore_index=True)
                  #print(query_df)
      #print(output_df)
      return output_df

"""
# must change -> param, bdate, edate, state, county
pollute_param = {   "42102": "Carbon dioxide", "43201": "Methane", "42401": "Sulfur dioxide", 
                    "42603": "Oxides of nitrogen(NOx)", "42101": "Carbon monoxide"
                }
"""

#-> focus on NYC:
{"code": "061", "value_represented": "New York"}      #--> skip; unindexable on EPA website..
{"code": "005", "value_represented": "Bronx"}         # Bronx
{"code": "047", "value_represented": "Kings"}         # Brooklyn
{"code": "081", "value_represented": "Queens"}        # Queens
{"code": "085", "value_represented": "Richmond"}      # Staten Island


# get elements / pollutant parameters.
# "https://aqs.epa.gov/data/api/list/parametersByClass?email=Hilarion.Reyes12@myhunter.cuny.edu&key=amberram68&pc=ALL"
      # CO2, Methane, SO2, NOx, CO, NITROUS OXIDE
pollute_param = ["42102","43201","42401","42603","42101","42605"]

# GENERATE CSV files for indexing data 
# (as opposed to constantly running web queries to obtain data)
"""
manhattan_df = generate_county_df(base_query, pollute_param, "061")
#manhattan_df.to_csv("manhattan.csv")

bronx_df = generate_county_df(base_query,pollute_param,"005")
#bronx_df.to_csv("bronx.csv")
print(bronx_df)

brooklyn_df = generate_county_df(base_query,pollute_param,"047")
#brooklyn_df.to_csv("brooklyn.csv")

queens_df = generate_county_df(base_query,pollute_param,"081")
#queens_df.to_csv("queens.csv")

staten_island_df = generate_county_df(base_query,pollute_param,"085")
#staten_island_df.to_csv("staten_island.csv")
"""

#===========================================#
""" #COLLECTIVE New York State county codes.
num_list = [str(i) for i in range(1, 124, 2)]
#print(num_list)
for i in range(len(num_list)):
    if len(num_list[i]) == 2:
        num_list[i] = "0" + num_list[i]
    if len(num_list[i]) == 1:
        num_list[i] = "00" + num_list[i]

NY_df = pd.DataFrame()
for value in num_list:
      df = generate_county_df(base_query,pollute_param,value)
      NY_df = NY_df.append(df, ignore_index=True)
NY_df.to_csv("newyork.csv")
""" # Not Used for our analysis -> only focused on NYC

#==========================================#
#VISUALIZATION:
"""
seaborn documentation:
==
https://seaborn.pydata.org/generated/seaborn.barplot.html
https://stackoverflow.com/questions/36220829/fine-control-over-the-font-size-in-seaborn-plots-for-academic-papers/36222162
"""
import seaborn as sns
import matplotlib.pyplot as plt

# run on 5 major boroughs: (mainly 3)
# bronx, brooklyn (empty), queens, staten island (empty), manhattan
# -> empty = SKIP
qtN_to_qtNplus1 = ['_to_2019_q1', '2019_q1_to_2019_q2', '2019_q2_to_2019_q3', '2019_q3_to_2019_q4',
                   '2019_q4_to_2020_q1', '2020_q1_to_2020_q2', '2020_q2_to_2020_q3', '2020_q3_to_2020_q4',
                   '2020_q4_to_2021_q1', '2021_q1_to_2021_q2', '2021_q2_to_2021_q3', '2021_q3_to_2021_q4']

#=====================#
#BRONX VISUALIZATION + ANALYSIS 
bronx_df = pd.read_csv("bronx.csv",index_col=False)
"""
#SO2_1hour_2010
bar_bronx_SO2_2010 = sns.barplot(x="yr_quarter", y="arithmetic_mean", 
                 data=bronx_df.loc[((bronx_df['parameter'] == 'Sulfur dioxide') & 
                 (bronx_df['pollutant_standard'] == 'SO2 1-hour 2010'))], estimator=np.median)
                 
print("bronx_SO2_1hour_2010_TABLE")
print(bronx_df[['site_number','observation_count','observation_percent',
      'arithmetic_mean','minimum_value','maximum_value','yr_quarter']].loc[(
                  (bronx_df['parameter'] == 'Sulfur dioxide') &
                  (bronx_df['pollutant_standard'] == 'SO2 1-hour 2010'))]) 

plt.figsize=(12, 8)
plt.xticks(rotation=45, fontsize=8)
#plt.savefig('bronx_SO2_1hour_2010_boxplot.png', dpi=100)
plt.show()
"""
"""
#SO2_Annual_1971 --> SKIP --> the same valuation observations for each given yr_quarter
bar_bronx_SO2_1971 = sns.barplot(x="yr_quarter", y="arithmetic_mean", 
                 data=bronx_df.loc[((bronx_df['parameter'] == 'Sulfur dioxide') & 
                 (bronx_df['pollutant_standard'] == 'SO2 Annual 1971'))], estimator=np.median)
                 
print("bronx_SO2_Annual_1971_TABLE")
print(bronx_df[['site_number','observation_count','observation_percent',
      'arithmetic_mean','minimum_value','maximum_value','yr_quarter']].loc[(
                  (bronx_df['parameter'] == 'Sulfur dioxide') &
                  (bronx_df['pollutant_standard'] == 'SO2 Annual 1971'))]) 

plt.figsize=(12, 8)
plt.xticks(rotation=45, fontsize=8)
#plt.savefig('bronx_SO2_Annual_1971_boxplot.png', dpi=100)
plt.show()
"""
"""
#SO2 values same, only need 1 pct_change lineplot
# site 110
bronx_SO2_pct_change_site110 = np.array(bronx_df[['arithmetic_mean']].loc[(
      (bronx_df['parameter'] == 'Sulfur dioxide') &
      (bronx_df['pollutant_standard'] == 'SO2 Annual 1971') &
      (bronx_df['site_number'] == 110))]
      .pct_change().values)
bronx_SO2_pct_change_site110 = unpack_pct_change_list(bronx_SO2_pct_change_site110)

print("bronx_SO2_pct_change_site110_TABLE")
pct_change_df = pd.concat(
    [pd.Series(bronx_SO2_pct_change_site110), pd.Series(qtN_to_qtNplus1)], axis=1) \
    .rename(columns={0: "pct_change", 1: "time_quarter"})
print(pct_change_df)

line_bronx_SO2_pct = sns.lineplot(x="time_quarter", y="pct_change", data=pct_change_df)
plt.figsize=(12, 8)
plt.axhline(y=0, color='black', linewidth=1.3, alpha=.7)
plt.xticks(rotation=15, fontsize=5.5)
plt.xlabel("time_quarter", fontsize=6)
#plt.savefig('bronx_SO2_pct_site110_lineplot.png', dpi=100)
plt.show()

# site 133
bronx_SO2_pct_change_site133 = np.array(bronx_df[['arithmetic_mean']].loc[(
      (bronx_df['parameter'] == 'Sulfur dioxide') &
      (bronx_df['pollutant_standard'] == 'SO2 Annual 1971') &
      (bronx_df['site_number'] == 133))]
      .pct_change().values)
bronx_SO2_pct_change_site133 = unpack_pct_change_list(bronx_SO2_pct_change_site133)

print("bronx_SO2_pct_change_site133_TABLE")
pct_change_df = pd.concat(
    [pd.Series(bronx_SO2_pct_change_site133), pd.Series(qtN_to_qtNplus1)], axis=1) \
    .rename(columns={0: "pct_change", 1: "time_quarter"})
print(pct_change_df)

line_bronx_SO2_pct = sns.lineplot(x="time_quarter", y="pct_change", data=pct_change_df)
plt.figsize=(12, 8)
plt.axhline(y=0, color='black', linewidth=1.3, alpha=.7)
plt.xticks(rotation=15, fontsize=5.5)
plt.xlabel("time_quarter", fontsize=6)
#plt.savefig('bronx_SO2_pct_site133_lineplot.png', dpi=100)
plt.show()
""" 
"""
#Oxides of nitrogen (NOx)
bar_bronx_NOx_ = sns.barplot(x="yr_quarter", y="arithmetic_mean", 
                 data=bronx_df.loc[((bronx_df['parameter'] == 'Oxides of nitrogen (NOx)')
                 )], estimator=np.median)
                 
print("bronx_NOx_TABLE")
print(bronx_df[['site_number','observation_count','observation_percent',
      'arithmetic_mean','minimum_value','maximum_value','yr_quarter']].loc[(
                  (bronx_df['parameter'] == 'Oxides of nitrogen (NOx)') 
                  )]) 
 
plt.figsize=(12, 8)
plt.xticks(rotation=45, fontsize=8)
#plt.savefig('bronx_NOx_boxplot.png', dpi=100)
plt.show()

# NOx_pct_change
bronx_NOx_pct_change = np.array(bronx_df[['arithmetic_mean']].loc[(
    (bronx_df['parameter'] == 'Oxides of nitrogen (NOx)')
)].pct_change().values)
bronx_NOx_pct_change = unpack_pct_change_list(bronx_NOx_pct_change)

print("bronx_NOx_pct_change_TABLE")
pct_change_df = pd.concat(
    [pd.Series(bronx_NOx_pct_change), pd.Series(qtN_to_qtNplus1)], axis=1) \
    .rename(columns={0: "pct_change", 1: "time_quarter"})
print(pct_change_df)

line_bronx_NOx_pct = sns.lineplot(x="time_quarter", y="pct_change", data=pct_change_df)
plt.figsize=(12, 8)
plt.axhline(y=0, color='black', linewidth=1.3, alpha=.7)
plt.xticks(rotation=15, fontsize=5.5)
plt.xlabel("time_quarter", fontsize=6)
#plt.savefig('bronx_NOx_pct_lineplot.png', dpi=100)
plt.show()
"""
"""
#CO
bar_bronx_CO_ = sns.barplot(x="yr_quarter", y="arithmetic_mean", 
                 data=bronx_df.loc[((bronx_df['parameter'] == 'Carbon monoxide')
                 )], estimator=np.median)
                 
print("bronx_CO_TABLE")
print(bronx_df[['site_number','observation_count','observation_percent',
      'arithmetic_mean','minimum_value','maximum_value','yr_quarter']].loc[(
                  (bronx_df['parameter'] == 'Carbon monoxide') 
                  )]) 
 
plt.figsize=(12, 8)
plt.xticks(rotation=45, fontsize=8)
#plt.savefig('bronx_CO_boxplot.png', dpi=100)
plt.show()

# CO_pct_change
bronx_CO_pct_change = np.array(bronx_df[['arithmetic_mean']].loc[(
    (bronx_df['parameter'] == 'Carbon monoxide')
)].pct_change().values)
bronx_CO_pct_change = unpack_pct_change_list(bronx_CO_pct_change)

print("bronx_CO_pct_change_TABLE")
pct_change_df = pd.concat(
    [pd.Series(bronx_CO_pct_change), pd.Series(qtN_to_qtNplus1)], axis=1) \
    .rename(columns={0: "pct_change", 1: "time_quarter"})
print(pct_change_df)

line_bronx_CO_pct = sns.lineplot(x="time_quarter", y="pct_change", data=pct_change_df)
plt.figsize=(12, 8)
plt.axhline(y=0, color='black', linewidth=1.3, alpha=.7)
plt.xticks(rotation=15, fontsize=5.5)
plt.xlabel("time_quarter", fontsize=6)
#plt.savefig('bronx_CO_pct_lineplot.png', dpi=100)
plt.show()
"""

#=====================#
# QUEENS VISUALIZATION + ANALYSIS
queens_df = pd.read_csv("queens.csv",index_col=False)

"""
# 'SO2 1-hour 2010'
bar_queens_SO2_2010 = sns.barplot(x="yr_quarter", y="arithmetic_mean", 
                 data=queens_df.loc[((queens_df['parameter'] == 'Sulfur dioxide') & 
                 (queens_df['pollutant_standard'] == 'SO2 1-hour 2010'))], estimator=np.median)
                 
print("queens_SO2_1hour_2010_TABLE")
print(queens_df[['site_number','observation_count','observation_percent',
      'arithmetic_mean','minimum_value','maximum_value','yr_quarter']].loc[(
                  (queens_df['parameter'] == 'Sulfur dioxide') &
                  (queens_df['pollutant_standard'] == 'SO2 1-hour 2010'))])


# 'SO2 Annual 1971'
bar_queens_SO2_1971 = sns.barplot(x="yr_quarter", y="arithmetic_mean", 
                 data=queens_df.loc[((queens_df['parameter'] == 'Sulfur dioxide') & 
                 (queens_df['pollutant_standard'] == 'SO2 Annual 1971'))], estimator=np.median)
                 
print("queens_SO2_Annual_1971_TABLE")
print(queens_df[['site_number','observation_count','observation_percent',
      'arithmetic_mean','minimum_value','maximum_value','yr_quarter']].loc[(
                  (queens_df['parameter'] == 'Sulfur dioxide') &
                  (queens_df['pollutant_standard'] == 'SO2 Annual 1971'))]) 

plt.figsize=(12, 8)
plt.xticks(rotation=45, fontsize=8)
#plt.savefig('queens_SO2_Annual_1971_boxplot.png', dpi=100)
plt.show()
"""
"""
#SO2 values same, only need 1 pct_change lineplot
queens_SO2_pct_change = np.array(queens_df[['arithmetic_mean']].loc[(
      (queens_df['parameter'] == 'Sulfur dioxide') &
      (queens_df['pollutant_standard'] == 'SO2 Annual 1971') &
      (queens_df['site_number'] == 124))]
      .pct_change().values)
queens_SO2_pct_change = unpack_pct_change_list(queens_SO2_pct_change)

print("queens_SO2_pct_change_TABLE")
pct_change_df = pd.concat(
    [pd.Series(queens_SO2_pct_change), pd.Series(qtN_to_qtNplus1)], axis=1) \
    .rename(columns={0: "pct_change", 1: "time_quarter"})
print(pct_change_df)

line_queens_SO2_pct = sns.lineplot(x="time_quarter", y="pct_change", data=pct_change_df)
plt.figsize=(12, 8)
plt.axhline(y=0, color='black', linewidth=1.3, alpha=.7)
plt.xticks(rotation=15, fontsize=5.5)
plt.xlabel("time_quarter", fontsize=6)
#plt.savefig('queens_SO2_pct_lineplot.png', dpi=100)
plt.show()
"""
"""
#=====#
# NOx
bar_queens_NOx = sns.barplot(x="yr_quarter", y="arithmetic_mean", 
                 data=queens_df.loc[((queens_df['parameter'] == 'Oxides of nitrogen (NOx)') 
                 )], estimator=np.median)
                 
print("queens_NOx_TABLE")
print(queens_df[['site_number','observation_count','observation_percent',
      'arithmetic_mean','minimum_value','maximum_value','yr_quarter']].loc[(
                  (queens_df['parameter'] == 'Oxides of nitrogen (NOx)')
                  )]) 

plt.figsize=(12, 8)
plt.xticks(rotation=45, fontsize=8)
#plt.savefig('queens_NOx_boxplot.png', dpi=100)
plt.show()
"""
"""
#site 124
queens_NOx_pct_change_site124 = np.array(queens_df[['arithmetic_mean']].loc[(
      (queens_df['parameter'] == 'Oxides of nitrogen (NOx)') &
      (queens_df['site_number'] == 124))]
      .pct_change().values)
queens_NOx_pct_change_site124 = unpack_pct_change_list(queens_NOx_pct_change_site124)

print("queens_NOx_pct_change_site124_TABLE")
pct_change_df = pd.concat(
    [pd.Series(queens_NOx_pct_change_site124), pd.Series(qtN_to_qtNplus1)], axis=1) \
    .rename(columns={0: "pct_change", 1: "time_quarter"})
print(pct_change_df)

line_queens_SO2_pct = sns.lineplot(x="time_quarter", y="pct_change", data=pct_change_df)
plt.figsize=(12, 8)
plt.axhline(y=0, color='black', linewidth=1.3, alpha=.7)
plt.xticks(rotation=15, fontsize=5.5)
plt.xlabel("time_quarter", fontsize=6)
#plt.savefig('queens_NOx_pct_lineplot_site124.png', dpi=100)
plt.show()

#site 125
queens_NOx_pct_change_site125 = np.array(queens_df[['arithmetic_mean']].loc[(
      (queens_df['parameter'] == 'Oxides of nitrogen (NOx)') &
      (queens_df['site_number'] == 125))]
      .pct_change().values)
queens_NOx_pct_change_site125 = unpack_pct_change_list(queens_NOx_pct_change_site125)

print("queens_NOx_pct_change_site125_TABLE")
pct_change_df = pd.concat(
    [pd.Series(queens_NOx_pct_change_site125), pd.Series(qtN_to_qtNplus1)], axis=1) \
    .rename(columns={0: "pct_change", 1: "time_quarter"})
print(pct_change_df)

line_queens_SO2_pct = sns.lineplot(x="time_quarter", y="pct_change", data=pct_change_df)
plt.figsize=(12, 8)
plt.axhline(y=0, color='black', linewidth=1.3, alpha=.7)
plt.xticks(rotation=15, fontsize=5.5)
plt.xlabel("time_quarter", fontsize=6)
#plt.savefig('queens_NOx_pct_lineplot_site125.png', dpi=100)
plt.show()
"""
"""
#=====#
# CO
bar_queens_CO = sns.barplot(x="yr_quarter", y="arithmetic_mean", 
                 data=queens_df.loc[((queens_df['parameter'] == 'Carbon monoxide') 
                 )], estimator=np.median)
                 
print("queens_CO_TABLE")
print(queens_df[['site_number','observation_count','observation_percent',
      'arithmetic_mean','minimum_value','maximum_value','yr_quarter']].loc[(
                  (queens_df['parameter'] == 'Carbon monoxide')
                  )]) 

plt.figsize=(12, 8)
plt.xticks(rotation=45, fontsize=8)
#plt.savefig('queens_CO_boxplot.png', dpi=100)
plt.show()
"""
"""
#site 124
queens_CO_pct_change_site124 = np.array(queens_df[['arithmetic_mean']].loc[(
      (queens_df['parameter'] == 'Carbon monoxide') &
      (queens_df['site_number'] == 124))]
      .pct_change().values)
queens_CO_pct_change_site124 = unpack_pct_change_list(queens_CO_pct_change_site124)

print("queens_CO_pct_change_site124_TABLE")
pct_change_df = pd.concat(
    [pd.Series(queens_CO_pct_change_site124), pd.Series(qtN_to_qtNplus1)], axis=1) \
    .rename(columns={0: "pct_change", 1: "time_quarter"})
print(pct_change_df)

line_queens_CO_pct = sns.lineplot(x="time_quarter", y="pct_change", data=pct_change_df)
plt.figsize=(12, 8)
plt.axhline(y=0, color='black', linewidth=1.3, alpha=.7)
plt.xticks(rotation=15, fontsize=5.5)
plt.xlabel("time_quarter", fontsize=6)
#plt.savefig('queens_CO_pct_lineplot_site124.png', dpi=100)
plt.show()

#site 125
queens_CO_pct_change_site125 = np.array(queens_df[['arithmetic_mean']].loc[(
      (queens_df['parameter'] == 'Carbon monoxide') &
      (queens_df['site_number'] == 125))]
      .pct_change().values)
queens_CO_pct_change_site125 = unpack_pct_change_list(queens_CO_pct_change_site125)

print("queens_CO_pct_change_site125_TABLE")
pct_change_df = pd.concat(
    [pd.Series(queens_CO_pct_change_site125), pd.Series(qtN_to_qtNplus1)], axis=1) \
    .rename(columns={0: "pct_change", 1: "time_quarter"})
print(pct_change_df)

line_queens_CO_pct = sns.lineplot(x="time_quarter", y="pct_change", data=pct_change_df)
plt.figsize=(12, 8)
plt.axhline(y=0, color='black', linewidth=1.3, alpha=.7)
plt.xticks(rotation=15, fontsize=5.5)
plt.xlabel("time_quarter", fontsize=6)
#plt.savefig('queens_CO_pct_lineplot_site125.png', dpi=100)
plt.show()
"""

#=====================#
# MANHATTAN VISUALIZATION + ANALYSIS
#=====#
manhattan_df = pd.read_csv("manhattan.csv",index_col=False)

"""
# CO
bar_manhattan_CO = sns.barplot(x="yr_quarter", y="arithmetic_mean", 
                 data=manhattan_df.loc[((manhattan_df['parameter'] == 'Carbon monoxide') 
                 )], estimator=np.median)
                 
print("manhattan_CO_TABLE")
print(manhattan_df[['site_number','observation_count','observation_percent',
      'arithmetic_mean','minimum_value','maximum_value','yr_quarter']].loc[(
                  (manhattan_df['parameter'] == 'Carbon monoxide')
                  )]) 

plt.figsize=(12, 8)
plt.xticks(rotation=45, fontsize=8)
plt.savefig('manhattan_CO_boxplot.png', dpi=100)
plt.show()
"""
"""
manhattan_CO_pct_change = np.array(manhattan_df[['arithmetic_mean']].loc[(
      (manhattan_df['parameter'] == 'Carbon monoxide')
      )]
      .pct_change().values)
manhattan_CO_pct_change = unpack_pct_change_list(manhattan_CO_pct_change)

print("manhattan_CO_pct_change_TABLE")
pct_change_df = pd.concat(
    [pd.Series(manhattan_CO_pct_change), pd.Series(qtN_to_qtNplus1)], axis=1) \
    .rename(columns={0: "pct_change", 1: "time_quarter"})
print(pct_change_df)

line_manhattan_CO_pct = sns.lineplot(x="time_quarter", y="pct_change", data=pct_change_df)
plt.figsize=(12, 8)
plt.axhline(y=0, color='black', linewidth=1.3, alpha=.7)
plt.xticks(rotation=15, fontsize=5.5)
plt.xlabel("time_quarter", fontsize=6)
#plt.savefig('manhattan_CO_pct_lineplot.png', dpi=100)
plt.show()
"""
