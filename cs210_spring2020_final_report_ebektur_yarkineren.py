# -*- coding: utf-8 -*-
"""CS210-Spring2020-Final Report_ebektur_yarkineren.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1izFTuLnktmvvgYtiEEBjLpxCmqSTO_I5

<font color="red">IMPORTANT</font>

<font color="red">This is just a template for the final report. You do not have to use the exact structure here. You may add your own sections. However, you are required to preserve the same report flow.</font>

# Airbnb Search

Group Members:

Yarkin Eren 
Eylul Bektur

## Introduction

This study focuses on what might be the leading reasons behind preferences of customers that intend to stay more than 30 days in a shared house in NYC, via AirBnb. This study aims to elaborate on why some shared rooms that have similar physical conditions with the popular options tend to remain unoccupied. As it is assumed that choice towards a shared room for a long stay may suggest purpose of stay might be different than tourism, research aims attention at the evidence that might be a reason for long term residence such as education and business. Therefore, distance of the hiring businesses and colleges between the AirBnb will be investigated through additional datas. In addition, crime rates for the location of Airbnb will be analysed with the help of the additional data as it is one of the main concerns for people when they choose a place to live. Besides the factors related with location and physical condition of the room, "feeling of attachment with the host" may be resulted in highly reserved shared rooms. This trust may be achieved by the language that hosts use in the description section, which is manipulated with the "safe terms" that are mostly appreciated by the visitors. Therefore, this marketing strategy with the usage of some guaranteed words will be examined by comparing availability rates of houses that have similar properties.
<font color="blue">
Briefly discuss the background and the rationale of the project.
</font>

### Problem Definition

<font color="blue">
State your problem in technical terms. What is your end goal? How are you going to solve it?

Our end goal is to determine what factors determine the preference according to our limitations. As it is assumed that newcomer or low-income immigrants would more likely to stay in a shared room, distance calculations were made for one of the most accurate group that fits into this situation: students. Along with some coding, we created a column that show the nearest distance between a house and university. Apart from distance of houses to universities, distance to crime is also extracted to eliminate some dangerous strees and parts of the city. Therefore, our data mainly is based on distance calculations to certain factors to find our accuracy among how accurate is our model for our occasion. However, besides distance calculations, popular terms are extracted from original AirBnb data and used for finding how it works for occupancy of houses. These popular words eliminated from adverbs since it does not contribute to overall preference. Word selections including street names, properties of house and popular adjective eventually contributes to popularity of the house. Marketing is an important element for house rental and it affect the availability as well without any factors for consideration.

</font>

### Utilized Datasets

<font color="blue">
Describe the utilized datasets in detail. Provide the data source (links if possible), number of obervations, data types, display the distributions of various variables and plot figures that helps reader understand what you are dealing with.

We have utizilized three different datasets in order to get a better understandment about issue we have chosen.
- ***NYC Airbnb Data***: 
This is our main data. 
- **Colleges and Universities around NYC**: In this data we have the locations of the colleges and universites that teach in NYC
- **NYC Arrest Data**: .


</font>

## Data Exploration

<font color="blue">
Explore the relationship between different variables across datasets. Perform hypothesis tests if necessary. Comment on your resulting figures and findings.

As the resarch is based on airbnb houses that offers shared for minimum 30 days, data is eliminated by these conditions. New dataframes created from the column called "neighbourhood_group" in the airbnb data in order to show the datas borough by borough.

From the official online sources of NYC. The enigma of zip codes has been solved. The zip codes extracted from the column named "zip" and put in column named "zip_by_borough".

In the university dataframe the longtitude and lattitude extracted from the column called "the_geom" by string manipulations and put in two different columns named "longtitude" and "latitude". We used this columns and created a new series object called "c", which gives the coordinates of the universities and colleges in NYC.
Then, in order to find minimum distance between a university for each accomodation, university data is grouped according to universities' neighbourhood. For each house in its neighbourhood, distance of universities is calculated. Lastly, the nearest is one is taken for the new column which is called min_distance. 

For marketing factors that is discussed in the hypothesis, name column of AirBnb data was manipulated in two ways. First, popular phrases which is used among all houses in the dataset were collected and transferred into new dataframe. As an additional information, a new column is extracted from description of houses that has higher occupation rate than the average and it transferred into created dataframe. In order to prepare a decent visualization, null values were filled with 0. 

Adjectives from description of houses that are more occupied are taken. Then, each house (including less occupied ones) is given a point by the frequency for usage of popular adjectives and put in a column called words_score. For feature engineering purposes, among all houses, scores are sorted in descending order. First 25 houses are stored in the column, which is equal to the number of houses that has higher occupancy rate than average. 

To utilize crime data in our dataset, we extracted number of crimes per neighbournood and used it in a new column called arrest_num in our original dataframe. 


This section corresponds to the work you have done in the progress report.
</font>

In this part we will show how we manipulate the and create new data out of the datas that we have.
"""

from google.colab import drive
drive.mount("/content/drive", force_remount=True)

path_prefix = "/content/drive/My Drive"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os.path import join
df_jobs=pd.read_csv(join(path_prefix, "NYC_Jobs.csv"))
df_arrest=pd.read_csv(join(path_prefix, "NYPD_Arrest_Data__Year_to_Date_.csv"))
df_unis=pd.read_csv(join(path_prefix, "COLLEGE_UNIVERSITY.csv"))
df=pd.read_csv(join(path_prefix, "AB_NYC_2019.csv"))
import seaborn as sns
import folium
from folium.plugins import HeatMap
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import geopy.distance
import pandas
from sklearn.preprocessing import StandardScaler
from geopy.distance import vincenty
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from matplotlib.colors import ListedColormap
from sklearn.model_selection import cross_val_score
from scipy import stats

"""All of the datas and the certain tools that will be used in this final report. are imported and included to colab. """

def meancal(df):
  a=0
  n=0
  for i in df["availability_365"]:
    a=i+a
    n=n+1
  mean_of_ava=a/n
  return mean_of_ava

def boro_categorize(boro_name):
 
    if (boro_name == "Q"):
        return "Queens"
    elif (boro_name == "S"):
       return "Staten Island"
    elif (boro_name == "K"):
      return "Brooklyn"
    elif (boro_name == "M"):
       return "Manhattan"
    elif (boro_name == "B"):
       return "Bronx"
    else:
      return "Non-defined"  

def zip_categorize(zip):

    if (9999 < zip <= 10099):
        return "Manhattan"
    elif (11299 < zip <= 11399):
       return "Queens"
    elif (10299 < zip <= 10399):
      return "Staten Island"
    elif (11199 < zip <= 11299):
       return "Brooklyn"
    elif (10399 < zip <= 10499):
       return "Bronx"
    else:
      return "Non-defined"

def visualize_model(model, data, labels, ax, title):
  step = 0.05

  cmap_light = ListedColormap(['orange', 'cyan', 'cornflowerblue'])
  cmap_bold = ListedColormap(['darkorange', 'c', 'darkblue'])

  model.fit(data, labels)

  x_min = data[:, 0].min() - 1
  x_max = data[:, 0].max() + 1
  y_min = data[:, 1].min() - 1
  y_max = data[:, 1].max() + 1

  xx, yy = np.meshgrid(np.arange(x_min, x_max, step), np.arange(y_min, y_max, step))
  y_pred = model.predict(np.hstack([xx.reshape(-1,1), yy.reshape(-1,1)])).reshape(xx.shape)

  ax.pcolormesh(xx, yy, y_pred, cmap=cmap_light)
  ax.scatter(data[:, 0], data[:, 1], c=labels, cmap=cmap_bold, edgecolor='k', s=20)
  ax.set_xlim(xx.min(), xx.max())
  ax.set_ylim(yy.min(), yy.max())
  ax.set_title(title)

"""These are the functions that we use for the data exploration."""

df_updated=df[df["room_type"]== "Shared room"]
df_updated=df_updated[df_updated["minimum_nights"] >= 30]
df_bronx=df_updated[df_updated["neighbourhood_group"] == "Bronx"]
df_manhattan=df_updated[df_updated["neighbourhood_group"] == "Manhattan"]
df_brooklyn=df_updated[df_updated["neighbourhood_group"] == "Brooklyn"]
df_queens=df_updated[df_updated["neighbourhood_group"] == "Queens"]
df_staten_island=df_updated[df_updated["neighbourhood_group"] == "Staten Island"]
bronx_mean=meancal(df_bronx)
manhattan_mean=meancal(df_manhattan)
brooklyn_mean=meancal(df_brooklyn)
queens_mean=meancal(df_queens)
all_mean=meancal(df_updated)
print(all_mean,queens_mean,brooklyn_mean,manhattan_mean,bronx_mean)

"""In this piece of code, houses that minimum duration of stay is bigger or equal to thirty has taken. All the means of staying empty per the neighborhood and the whole New York are calculated in order to understand, which neighborhood tends to stay empty."""

df_arrest['Arrest_location'] = df_arrest["ARREST_BORO"].apply(boro_categorize)
br,mh,bx,qs,si=df_arrest['Arrest_location'].value_counts()
df_updated["arrest_num"]=""
for i in range(107):
  if df_updated["neighbourhood_group"].iloc[i]=="Manhattan":
    df_updated["arrest_num"].iloc[i]=mh
  elif df_updated["neighbourhood_group"].iloc[i]=="Brooklyn":
    df_updated["arrest_num"].iloc[i]=br
  elif df_updated["neighbourhood_group"].iloc[i]=="Bronx":
    df_updated["arrest_num"].iloc[i]=bx
  elif df_updated["neighbourhood_group"].iloc[i]=="Queens":
    df_updated["arrest_num"].iloc[i]=qs
  elif df_updated["neighbourhood_group"].iloc[i]=="Staten Island":
    df_updated["arrest_num"].iloc[i]=si

"""From the NYPD dataset, the arrest locations' neighborhoods are extracted and a new cloumn is created to store the data.

The number of arrests are counted and stored in variables per neighborhood. Then a new column is created in order to store the how many arrests made per neighborhood.
"""

df_unis['ZIP'] = df_unis['ZIP'].astype(int)
df_unis['Borough_from_ZIP'] = df_unis["ZIP"].apply(zip_categorize)

"""From the zip code colunm of the university data, all neighborhood informations are extracted and putted in a new column called "Borough_from_zip" using zip_categorize function."""

df_unis['the_geom'].str.strip('( )') 
df_unis ['Longitude']= df_unis['the_geom'].str.split(' ', expand = True)[1]
df_unis ['Lattitude']= df_unis['the_geom'].str.split(' ', expand = True)[2]
df_unis["Lattitude"]=df_unis["Lattitude"].str.strip(')')
df_unis["Longitude"]=df_unis["Longitude"].str.strip('(')
df_unis.head()

"""Longtitudes and latitudes are extracted from the "the_geom" column of the university dataset by applying string manipulations."""

df_above_mean=df_updated[df_updated["availability_365"] < 272]
b=pd.Series(' '.join(df_above_mean['name']).lower().split()).value_counts()[:32]
a=pd.Series(' '.join(df_updated['name']).lower().split()).value_counts()[6:32]
a=a.fillna(0)
b=b.fillna(0),
df_updated["name"]=df_updated["name"].str.lower()
df_updated["words_score"]=0
words=["shared","room","space","great","coliving","comfortable","cozy","beatiful","apartment","manhattan","brooklyn"]
for j in range(107):
  for i in words:
    if i in df_updated["name"].iloc[j]:
      df_updated["words_score"].iloc[j]=df_updated["words_score"].iloc[j]+1
df_updated.sort_values(by=["words_score"],inplace=True,ascending=False)
df_updated_score=df_updated.head(25)
score=0
for i in range(25):
  for j in range(25):
    if df_updated_score["id"].iloc[i]==df_above_mean["id"].iloc[j]:
      score=score+1
print("the succes rate of using popular words is %",score*4)

"""In this piece of code, we counted what words used how many times for popular houses whose availability rate is lower than others in New York. We assumed that their use of language may influenced people to rent that house. Then, we compared it with that number of randomized set that includes both popular and unpopular houses. We compared those two sets and used for increasing accuracy score at later stages. Using feature engineering the null values in availability_365 column are filled with zeroes.




"""

df_unis['Longitude']=df_unis['Longitude'].astype(float)
df_unis['Lattitude']=df_unis['Lattitude'].astype(float)
df_updated['latitude']=df_updated['latitude'].astype(float)
df_updated['longitude']=df_updated['longitude'].astype(float)
df_updated["min_distance"]=""
list_distance = []
for i in range(107):
  if (df_updated["neighbourhood_group"].iloc[i]=='Manhattan'):
    
    list_distance=[]
    for j in range(77):
      if(df_unis["Borough_from_ZIP"].iloc[j]=='Manhattan'):
        
        lat1 = df_unis['Lattitude'].iloc[j]
        lon1 = df_unis['Longitude'].iloc[j]
        lat2 = df_updated['latitude'].iloc[i]
        lon2 = df_updated['longitude'].iloc[i]
        
        site_coords = (lat1,lon2)
        place2_coords = (lat2,lon2)
        distance=geopy.distance.vincenty(site_coords, place2_coords).km
        list_distance.append(distance)
    df_updated["min_distance"].iloc[i]=min(list_distance)
      
  elif (df_updated["neighbourhood_group"].iloc[i]=="Brooklyn"):
    list_distance=[]
    for j in range(77):
      if(df_unis["Borough_from_ZIP"][j]=="Brooklyn"):
        
        lat1 = df_unis['Lattitude'].iloc[j]
        lon1 = df_unis['Longitude'].iloc[j]
        lat2 = df_updated['latitude'].iloc[i]
        lon2 = df_updated['longitude'].iloc[i]
        
        site_coords = (lat1,lon2)
        place2_coords = (lat2,lon2)
        distance=geopy.distance.vincenty(site_coords, place2_coords ).km
        list_distance.append(distance)
        
    df_updated["min_distance"].iloc[i]=min(list_distance)
  elif (df_updated["neighbourhood_group"].iloc[i]=="Queens"):
    list_distance=[]
    for j in range(77):
      if(df_unis["Borough_from_ZIP"].iloc[j]=="Queens"):
        
        lat1 = df_unis['Lattitude'].iloc[j]
        lon1 = df_unis['Longitude'].iloc[j]
        lat2 = df_updated['latitude'].iloc[i]
        lon2 = df_updated['longitude'].iloc[i]
        
        site_coords = (lat1,lon2)
        place2_coords = (lat2,lon2)
        distance=geopy.distance.vincenty(site_coords, place2_coords).km
        list_distance.append(distance)

    df_updated["min_distance"].iloc[i]=min(list_distance)
  elif (df_updated["neighbourhood_group"].iloc[i]=="Staten Island"):
    list_distance=[]
    for j in range(77):
      if(df_unis["Borough_from_ZIP"].iloc[j]=="Staten Island"):
        
        lat1 = df_unis['Lattitude'].iloc[j]
        lon1 = df_unis['Longitude'].iloc[j]
        lat2 = df_updated['latitude'].iloc[i]
        lon2 = df_updated['longitude'].iloc[i]
        
        site_coords = (lat1,lon2)
        place2_coords = (lat2,lon2)
        distance=geopy.distance.vincenty(site_coords, place2_coords).km
        list_distance.append(distance)

    df_updated["min_distance"].iloc[i]=min(list_distance)
  elif (df_updated["neighbourhood_group"].iloc[i]=="Bronx"):
    list_distance=[]
    for j in range(77):
      if(df_unis["Borough_from_ZIP"].iloc[j]=="Bronx"):
        
        lat1 = df_unis['Lattitude'].iloc[j]
        lon1 = df_unis['Longitude'].iloc[j]
        lat2 = df_updated['latitude'].iloc[i]
        lon2 = df_updated['longitude'].iloc[i]
        
        site_coords = (lat1,lon2)
        place2_coords = (lat2,lon2)
        distance=geopy.distance.vincenty(site_coords, place2_coords ).km
        list_distance.append(distance)
    df_updated["min_distance"].iloc[i]=min(list_distance)   
df_updated.head()

"""In this piece of code, we calculated the distance of each house to its nearist university. In order to this task, the universities categorized to the neighborhoods they belong(to speed up the process). Then every houses' distance between the universities that in its neighborhood is calculated with geopy(coordinates) and the minimum is taken. After this process we create another column in dataset for storing the value of a house's minimum distance to an university called "min_distance".

## Machine Learning Model ##

### Implementation

<font color="blue">
Implement and evaluate your models. Perform hyperparameter tunning if necessary. Choose the correct evaluation metrics.
</font>
"""

k=8
df_updated["reviews_per_month"]=df_updated["reviews_per_month"].fillna(0)
X = df_updated[['min_distance',"arrest_num","words_score"]] 
y = df_updated['availability_365']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)
knn = KNeighborsClassifier(k, metric="euclidean")
knn.fit(X_train, y_train)
y_pred=knn.predict(X_test)
accuracyknnold = accuracy_score(y_test, y_pred)

y=df_updated["availability_365"]
X = df_updated[['min_distance',"arrest_num","words_score"]] 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)
model = tree.DecisionTreeClassifier()
model.fit(X_train, y_train)
y_pred=model.predict(X_test)
accuracydecold= accuracy_score(y_test, y_pred)

K_range = np.arange(1, 15)
accuracy_list = []

for k in K_range:
  knn = KNeighborsClassifier(k, metric="euclidean")
  knn.fit(X_train, y_train)
  y_pred = knn.predict(X_test)
  accuracy = accuracy_score(y_test, y_pred)
  accuracy_list.append(accuracy)

plt.figure(figsize=(12, 6))  
plt.plot(K_range, accuracy_list, color='black', linestyle='dashed', marker='o',  
         markerfacecolor='red', markersize=10)
plt.title('Accuracy of the Validation w/ K')  
plt.xlabel('K')  
plt.ylabel('Accuracy')
plt.xticks(K_range)
plt.grid()
plt.show()

"""In order to maximise the accuracy value, we tried k values in order to find the best fit. Therefore, it showed that clustring for 13 grops leads to best accuracy"""

k=13
df_updated["reviews_per_month"]=df_updated["reviews_per_month"].fillna(0)
X = df_updated[['min_distance',"arrest_num","words_score"]]
y = df_updated['availability_365']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)
knn = KNeighborsClassifier(k, metric="euclidean")
knn.fit(X_train, y_train)
y_pred=knn.predict(X_test)
accuracyknn = accuracy_score(y_test, y_pred)

accuracy_list = []
accuracy_SD_list = []
for depth in range(1,10):
  model = tree.DecisionTreeClassifier(max_depth=depth)
  accuracies_CV = cross_val_score(model, X_train, y_train, cv=10)
  accuracy_list.append(accuracies_CV.mean())
  accuracy_SD_list.append(accuracies_CV.std())
plt.figure(figsize=(12, 6))  
plt.plot(range(1, 10), accuracy_list, color='black', linestyle='solid')
plt.plot(range(1, 10), np.array(accuracy_list) + np.array(accuracy_SD_list),color='black', linestyle='dashed')
plt.plot(range(1, 10), np.array(accuracy_list) - np.array(accuracy_SD_list),color='black', linestyle='dashed' )
plt.fill_between(range(1, 10), np.array(accuracy_list) + np.array(accuracy_SD_list),
                 np.array(accuracy_list) - np.array(accuracy_SD_list), alpha=0.2, facecolor ='b')
plt.plot()
plt.title('10-fold cross validated accuracy w/ max_depth')  
plt.xlabel('Max depth')  
plt.ylabel('CV Accuracy +/- sd') 
plt.show()

"""Cross validation shows that proper max-depth that will be used for hypermeter tuning should be 5."""

y=df_updated["availability_365"]
X = df_updated[['min_distance',"arrest_num","words_score"]] 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)
model = tree.DecisionTreeClassifier(max_depth=5)
model.fit(X_train, y_train)
y_pred=model.predict(X_test)
accudec= accuracy_score(y_test, y_pred)

"""### Results & Discussion






"""

print(accuracyknn,accuracyknnold)

"""After a optimization of k value, our accuracy value rised to 0.36 from 0.27 which is more or less 33% increase."""

print(accuracydecold,accudec)

"""Accuracy of this model was around 0.18. However, as we used max_depth parameter which was optimised by 4, we can now obtain 0.27 accuracy."""

mean_distance=df_updated["min_distance"].mean()
above_mean = df_updated[df_updated["min_distance"] >= mean_distance]["availability_365"]  
below_mean = df_updated[df_updated["min_distance"] <mean_distance]["availability_365"]
fig, ax = plt.subplots(1,2) 
        
above_mean.plot(kind="hist", ax=ax[0], bins=20, label="completed", color="c")
ax[0].set_title("above from the mean")


below_mean.plot(kind="hist", ax=ax[1], bins=20, label="none", color="m")
ax[1].set_title("below from the mean")

"""Our null hyphotesis indicates that Houses near universities are more likely to be booked. In order to achieve this, we grouped houses as far and near. We agreed that distance that is below than average distance should be named as "near" and vice versa. For our second column, we chose availability_365 which shows occupation amount per year of a house. Therefore, when we applied T-test to evaluate our hypothesis, we came up with a p-value which is 0.13. As it was bigger than our significance value, which was 0.05, we assumed that null hypothesis is true. """

stats.ttest_ind(above_mean, below_mean, equal_var=False)

df_arrest['Arrest_location'].value_counts().plot(kind='bar')

"""We can see the Brooklyn is the neighborhood that most crimes were committed."""

df_unis['Borough_from_ZIP'].value_counts().plot(kind='pie')

"""This pie chart shows that, most of the universities in New York is in Manhattan."""

m = folium.Map(location=[ 40.730610, -73.935242], zoom_start=12, width=1000, height=500,tiles = "Stamen Terrain")
c=df_unis[["Lattitude", "Longitude"]].values
HeatMap(c,radius=30).add_to(m)
m

"""The heat map shows, the density of the universities in New York."""

c=df_updated[["latitude", "longitude"]].values
m = folium.Map(location=[ 40.730610, -73.935242], zoom_start=12, width=1000, height=500,tiles = "Stamen Terrain")
HeatMap(c,radius=30).add_to(m)
m

"""The heat map shows the density of the airbnb houses that minimum duration of stay more than 30 in New York.

## Conclusion

<font color="blue">
Briefly evaluate your project. Is your solution applicable? What are the advantages/disadvantages of your solution?
</font>

Our model is based on predicting vacancy of a shared room that requires minimum 30 days of stay by training 3 different data. We try taking our additional data such that dependency will be less, which would increase our accuracy for our result. 
We find our way of processing this project quite applicable, since new immigrants that has to shared a room is less likely a family or a employee that has well-profitted job. One of the main consideration for our target is distance to universities as we assumed students would benefit from shared room of minimum stay for a month. First, without using any additional data, we created a variable called 'frequency of usage of popular words in description'. Popular words was an well-fitted aspect for our research, since we extracted from original data. Therefore, we were 100% sure that all descriptions were iterated by reported AirBnb houses, and there is no overfitting. This directly affected our accuracy values, which is an advantage of this research. Along with contribution of NYC University Data, one of the most direct factor for our hypothesis was finding exact nearest distance for each house and university with geopy.distance. Therefore, this information directly affected our accuracy score. However, as we majorly focused on students as customers for our limitations, for further studies public transportation of NYC may also be used since students may choose to live far because of some other factor such as budget. 
Crime Data of NYC also showed positive correlation for demand to house rentals. Although it is quite minimal as it is compared to whole data, tax fellonies and other state law related crimes were recorded by NYPD. However, they might not be correlated with house rentals since it was not aiming to human itself but governmental institutions. For a better research, those crimes may be identified and neglected. 

In addition, for well-adjusted researches in the future, NYC Jobs Data should be included which also refers to employees that has low budgets. In the project proposal we thought we could add jobs into our project along the universities however, the address column of the jobs dataset was written by a human like a person writes his/her adress for letter receivement. Therefore we need a tool like google maps in order to get the correct location of the jobs but, unfortunately google's service was not free and, we could not add jobs into our project. (we tried offline free tools in order to replace google maps api but they did not work)

To conclude, we took our additional data such that dependency will be less, which would increase our accuracy for our result which made our research applicable.
"""