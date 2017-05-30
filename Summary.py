import pandas as pd 

#windows
rawdata = pd.read_csv('C:\\Users\\Barney\\Desktop\\E-Bike_Survey_Responses.csv',header=0)

#mac
cd "/Users/Barney/Desktop/"
rawdata = pd.read_csv('E-Bike_Survey_Responses.csv',header=0)

surveydata = rawdata.copy()

# I have no idea why this doesnt work...
surveydata.rename(columns = {0:'time', 1:'age', 3:'physical_health', 4:'education_level',\
5: 'household_income', 6: 'employment_category', 7: 'address_district', 8: 'avg_distance_travel_perweek',\
9: 'avg_travel_time', 10: 'transportation_type', 11: '#of_moterized_vechels', 12:'Support_document', 13:'when_to_use',\
14: 'aware_speed_limit', 15: 'visul_accident', 16: 'punishing', 17: 'moter_vehicle', 18: 'when_use_bike', 19: 'bike_lane',\
20: 'sidewalk_issue', 21: 'personal_mobility_devices'}, inplace=True)


surveydata = surveydata.rename(columns = {'Timestamp':'time', '1. What age range do you fall in?':'age', \
'How would you describe your level of physical health?':'physical_health', \
'What level of education have you reached?':'education_level',\
'What is your household income?': 'household_income', \
'Which category best describes your employment?': 'employment_category', \
'What Toronto district is your primary address located in?': 'address_district', \
'On average, what distance do you travel most days of the week?': 'avg_distance_travel_perweek',\
'On average, how long is your commute? (each way)': 'avg_travel_time', \
'Which transportation option do you end up using most often?': 'transportation_type', \
'Does your household have access to any of the following types of private motorized vehicles?': '#of_moterized_vechels', \
'Do you support any of the following statements?':'Support_document', \
"When you use Toronto's Multi-Use Trails do you mostly":'when_to_use',\
"Are you aware that the City of Toronto's Multi-Use Paths have a speed limit of 20 km/h?": 'aware_speed_limit', \
'Have you witnessed a collision or conflict on a trail between': 'visul_accident', \
'Do you think more should be done to manage trail users who do not respect the 20 km/h speed limit?': 'punishing', \
'Currently, any kind of e-bike may use a multi-use path if they are propelled by pedaling only.  If any e-biker or other type of vehicle is being propelled by motor power, then it is considered a motor vehicle, and may be fined.': 'moter_vehicle', \
"When you use Toronto's bicycle lanes do you mostly": 'when_use_bike', \
'Currently, any kind of e-bike may use a bicycle lane, provided they are propelled by pedalling only.  If any e-bike is being propelled by motor power, then it is considered a motor vehicle and may be fined. ': 'bike_lane',\
'Sidewalks are for pedestrians.  Cyclists and e-bikers should not ride or drive on sidewalks.  With regards to illegal use of bicycles and e-bikes on sidewalks, should the City.': 'sidewalk_issue', \
'Toronto Bylaws consider personal mobility devices (such as electric wheel chairs) to be pedestrians.  Historically, there has been little risk as electric wheelchairs available for purchase have only traveled at speeds which are close to walking speed.  More recently, personal mobility devices which resemble e-bikes and may travel at more than triple walking speed have become available.  In your opinion, should the City;': 'personal_mobility_devices'})
 

surveydata.head(n=1)

print(surveydata.describe())

# Understand who interviewed?

from pandasql import sqldf
pysqldf = lambda q: sqldf(q,globals())
  
querylist = []
for i in list(range(22)):
    query = '''SELECT count(*) as Num, ''' + str(surveydata.columns[i]) + ' FROM surveydata ' + 'GROUP BY ' + str(surveydata.columns[i]) + ''';'''
    querylist.append(query)

print (pysqldf(querylist[7]))


# build up the summary dataframe 
d = {'Gender':['Male', 'Female', 'NA', 'other'],
     'Number':[1554,657,51,10]}
Gender_result = pd.DataFrame(d)     

income_result = pd.DataFrame(pysqldf(querylist[5]))

region_summary = pd.DataFrame(pysqldf(querylist[7]))

test = region_summary.copy()
test[test.Num < 10].sum()

sum(test.Num>100)




testquery1 = '''SELECT Num, (CASE address_district
                WHEN Num<=10 THEN 'Others'
                ELSE address_district
                END)
                FROM region_summary;'''
                
print (pysqldf(testquery1))



# Visulization 
import matplotlib.pyplot as plt
 
labels = Gender_result.Gender
sizes = Gender_result.Number
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']

plt.pie(sizes, colors=colors, labels=labels, shadow=False, startangle=90)
plt.legend(patches, labels, loc="best")
plt.axis('equal')
#plt.tight_layout()
plt.show()




import plotly.plotly as py
import plotly.graph_objs as go

labels = Gender_result.Gender
values = Gender_result.Number

trace = go.Pie(labels=labels, values=values)
py.iplot([trace], filename='basic_pie_chart')









import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 5, 0.1);
y = np.sin(x)
plt.plot(x, y)






