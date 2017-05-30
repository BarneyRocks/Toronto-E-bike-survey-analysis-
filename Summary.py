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
 
 
############# Understand who interviewed?
from pandasql import sqldf
pysqldf = lambda q: sqldf(q,globals())
  
querylist = []
for i in list(range(22)):
    query = '''SELECT count(*) as Num, ''' + str(surveydata.columns[i]) + ' FROM surveydata ' + 'GROUP BY ' + str(surveydata.columns[i]) + ''';'''
    querylist.append(query)

print (pysqldf(querylist[7]))


####### Gender_Summary
d = {'Gender':['Male', 'Female', 'NA', 'other'],
     'Number':[1554,657,51,10]}
Gender_result = pd.DataFrame(d)     


####### Income Summary
income_result = pd.DataFrame(pysqldf(querylist[5]))
#income_result['household_income']=income_result['household_income'].replace('None','NA')


####### Region Summay
region_summary = pd.DataFrame(pysqldf(querylist[7]))

region_summaryq1 = '''SELECT SUM(a.Num), a.address_district
                      FROM (SELECT Num, 
                                CASE 
                                    WHEN Num<10 THEN 'Others'
                                    ELSE address_district
                                END AS address_district
                            FROM region_summary) as a
                      GROUP BY a.address_district;'''

region_summary_fixed = pd.DataFrame(pysqldf(region_summaryq1))




# Visulization 
import matplotlib.pyplot as plt


####### Gender_Summary
label_test = []
for i in list(range(4)):
    label_test.append(str(Gender_result.Gender[i]) + ' (' + str(Gender_result.Number[i]) + ')')

sizes = Gender_result.Number
colors = ["#E13F29", "#D69A80", "#D63B59", "#AE5552"]
patches, texts = plt.pie(sizes, colors=colors, startangle=90)
plt.legend(patches, label_test, loc="best")

plt.title('gender summary',y=1.08)
plt.axis('equal')
plt.tight_layout()
plt.show()



