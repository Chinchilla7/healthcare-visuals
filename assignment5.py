#load in packages to transform data
from this import d
import pandas as pd
import numpy as np

#load in packages to visualize data
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

sns.set_theme(style='whitegrid')

#load in data
dataframe = pd.read_csv('data/Georgia_COVID-19_Case_Data.csv')
dataframe

len(dataframe)
dataframe.shape

#describing variables
dataframe.info()

list(dataframe)

dataframe['COUNTY'].value_counts()

dataframe_counties = dataframe['COUNTY'].value_counts()
dataframe_counties.head(20)

#transforming columns
dataframe['DATESTAMP']

#creating copy of column
dataframe['DATESTAMP_MOD'] =dataframe['DATESTAMP']
print(dataframe['DATESTAMP_MOD'].head(10))
print(dataframe['DATESTAMP_MOD'].dtypes)

dataframe['DATESTAMP_MOD'] = pd.to_datetime(dataframe['DATESTAMP_MOD'])
dataframe['DATESTAMP_MOD'].dtypes

dataframe[['DATESTAMP','DATESTAMP_MOD']]

dataframe['DATESTAMP_MOD_DAY'] = dataframe['DATESTAMP_MOD'].dt.date
dataframe['DATESTAMP_MOD_DAY']

dataframe['DATESTAMP_MOD_YEAR'] = dataframe['DATESTAMP_MOD'].dt.year
dataframe['DATESTAMP_MOD_MONTH'] = dataframe['DATESTAMP_MOD'].dt.month
dataframe['DATESTAMP_MOD_YEAR'] 
dataframe['DATESTAMP_MOD_MONTH']

dataframe

dataframe['DATESTAMP_MOD_MONTH_YEAR'] = dataframe['DATESTAMP_MOD'].dt.to_period('M')
dataframe['DATESTAMP_MOD_MONTH_YEAR'].sort_values

dataframe

dataframe['DATESTAMP_MOD_WEEK'] = dataframe['DATESTAMP_MOD'].dt.isocalendar().week
dataframe['DATESTAMP_MOD_WEEK']

dataframe['DATESTAMP_MOD_QUARTER'] = dataframe['DATESTAMP_MOD'].dt.to_period('Q')
dataframe['DATESTAMP_MOD_QUARTER'].sort_values

dataframe['DATESTAMP_MOD_DAY_STRING'] = dataframe['DATESTAMP_MOD_DAY'].astype(str)
dataframe['DATESTAMP_MOD_WEEK_STRING'] = dataframe['DATESTAMP_MOD_WEEK'].astype(str)
dataframe['DATETIME_STRING'] = dataframe['DATESTAMP_MOD_MONTH_YEAR'].astype(str)

dataframe

#Getting counties required for analysis
#Counties we want to analyze: Cobb, DeKalb, Fulton, Gwinnett, Hall
dataframe['COUNTY']
countylist = ['COBB', 'DEKALB', 'FULTON', 'GWINNETT', 'HALL']
countylist

selectcounties = dataframe[dataframe['COUNTY'].isin(countylist)]
len(selectcounties)

#original dataframe length ~90,000
#selectcounties = length 2830
#selectcountiestimes = ?

#getting specific datetime frame
selectcountytime = selectcounties

selectcountytime['DATESTAMP_MOD_MONTH_YEAR']

selectcountytime_april2020 = selectcountytime[selectcountytime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-04']
len(selectcountytime_april2020)

selectcountytime_aprilmay2020 = selectcountytime[(selectcountytime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-05') | (selectcountytime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-04')]
len(selectcountytime_aprilmay2020)

selectcountytime_aprilmay2020.head(50)

#Creating final dataframe with certain columns only
finaldf = selectcountytime_aprilmay2020[['COUNTY',
                                        'DATESTAMP_MOD',
                                        'DATESTAMP_MOD_DAY',
                                        'DATESTAMP_MOD_DAY_STRING',
                                        'DATETIME_STRING',
                                        'DATESTAMP_MOD_MONTH_YEAR',
                                        'C_New', #cases - new
                                        'C_Cum', #cases - total
                                        'H_New', #hospitalizations - new
                                        'H_Cum', #hospitalizations -total
                                        'D_New', #deaths - new
                                        'D_Cum', #deaths - total
                                        ]]
finaldf

#Looking at total covid cases by month
finaldf_dropdups = finaldf.drop_duplicates(subset=['COUNTY', 'DATETIME_STRING'], keep='last')
finaldf_dropdups
import numpy as np
pd.pivot_table(finaldf_dropdups, values='C_Cum', index=['COUNTY'],
                columns=['DATESTAMP_MOD_MONTH_YEAR'], aggfunc=np.sum)

vis1 = sns.barplot(x='DATESTAMP_MOD_MONTH_YEAR', y='C_Cum', data=finaldf_dropdups)

vis2 = sns.barplot(x='DATESTAMP_MOD_MONTH_YEAR', y='C_Cum', hue="COUNTY", data=finaldf_dropdups)

plotly1 = px.bar(finaldf_dropdups, x='DATETIME_STRING', y='C_Cum', color='COUNTY', barmode='group')
plotly1.show()

plotly1 = px.bar(finaldf_dropdups, x='DATETIME_STRING', y='C_Cum', color='COUNTY', barmode='stack')
plotly1.show()

#Looking at total covid cases by day
daily = finaldf
daily
len(daily)

pd.pivot_table(daily, values='C_Cum', index=['COUNTY'],
                columns=['DATESTAMP_MOD_DAY'], aggfunc=np.sum)

TEMPdf = pd.pivot_table(daily, values='C_Cum', index=['DATESTAMP_MOD_DAY'],
                columns=['COUNTY'], aggfunc=np.sum)

TEMPdf.head(50)

startdate = pd.to_datetime("2020-04-26").date()
enddate = pd.to_datetime("2020-05-09").date()

maskFilter = (daily['DATESTAMP_MOD_DAY'] >= startdate) & (daily['DATESTAMP_MOD_DAY'] <= enddate)
dailyspecific = daily.loc[maskFilter]
dailyspecific

dailyspecific[dailyspecific['COUNTY'] == 'FULTON']

vis3 = sns.lineplot(data=dailyspecific, x='DATESTAMP_MOD_DAY', y="C_Cum")

vis4 = sns.lineplot(data=dailyspecific, x='DATESTAMP_MOD_DAY', y="C_Cum", hue='COUNTY')

plotly3 = px.bar(dailyspecific, x="DATESTAMP_MOD_DAY", y="C_Cum", color='COUNTY')
plotly3.show()

plotly4 = px.bar(dailyspecific, x="DATESTAMP_MOD_DAY", 
                                y="H_New", 
                                color='COUNTY',
                                barmode='group')
plotly4.show()

plotly5 = px.bar(dailyspecific, x="DATESTAMP_MOD_DAY", 
                                y="H_Cum", 
                                color='COUNTY',
                                barmode='group')
plotly5.show()

plotly6 = px.bar(dailyspecific, x="DATESTAMP_MOD_DAY", 
                                y="D_New", 
                                color='COUNTY',
                                barmode='group')
plotly6.show()

plotly7 = px.bar(dailyspecific, x="DATESTAMP_MOD_DAY", 
                                y="D_Cum", 
                                color='COUNTY',
                                barmode='group')
plotly7.show()

dailyspecific['NewHospandDeathCovid'] = dailyspecific['D_New'].astype(int) + dailyspecific['H_New'].astype(int) + dailyspecific['C_New'].astype(int)
dailyspecific['NewHospandDeathCovid']

dailyspecific['NewHospandDeath'] = dailyspecific['D_New'].astype(int) + dailyspecific['H_New'].astype(int) 
dailyspecific['NewHospandDeath']

dailyspecific

plotly8 = px.bar(dailyspecific, x="DATESTAMP_MOD_DAY", 
                                y="NewHospandDeath", 
                                color='COUNTY',
                                title='Georgia 2020 Covid Data: Total New Hospitalizations, Deaths, and Covid cases by County',
                                labels={
                                    "DATESTAMP_MOD_DAY": "Time (Month, Day, Year)",
                                    "NewHospandDeathCovid": "Total Count"
                                }, 
                                barmode='group')
plotly8.update_layout(
    xaxis = dict(tickmode='linear', type='category')
)
plotly8.show()







