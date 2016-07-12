import re
import json
import pandas as pd
import matplotlib
matplotlib.use('nbAgg')
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim

# ---------------------------------------------------------------------------------------------------------------------
#  Finding unique values

uniqueID       = tweets_full_dataframe.userID.unique()
uniqueLocation = tweets_full_dataframe.tweet_location.unique()
uniqueLanguage = tweets_full_dataframe.tweet_lang.unique()

print("There are %d tweets in this dataframe, but only %d unique users." %(len(tweets_full_dataframe), len(uniqueID)))
print("Of the %d unique users, there are %d different languages represented." %(len(uniqueID), len(uniqueLanguage)))
print("Of the %d unique users, %d listed a self-reported location." %(len(uniqueID), len(uniqueLocation)))

# ---------------------------------------------------------------------------------------------------------------------
# Of the tweets with self-reported locations in the user profile, how many also have geo-location from the tweet?
#  Determining how many tweets have both user-defined and GPS-defined (latitude, longitude) coordinates

tweets_w_UserLocation = tweets_full_dataframe[['userID','tweet_location','user_lats','user_lons']].dropna()
print("There are %d tweets with user defined locations.\n" %(len(tweets_w_UserLocation)))

tweets_w_GPSLocation = tweets_full_dataframe[['userID','geo_lats','geo_lons']].dropna()
print("There are %d tweets with GPS defined locations.\n" %(len(tweets_w_GPSLocation)))

tweets_w_Location = tweets_full_dataframe[['userID','tweet_location','user_lats','user_lons','geo_lats','geo_lons']].dropna()
print("From the %d tweets with user defined locations, %d also have GPS defined locations.\n"
      %(len(tweets_w_UserLocation), len(tweets_w_Location)))

uniqueUsers_w_Location = tweets_w_Location.userID.unique()
print("From the %d tweets with both user defined and GPS defined locations, %d are from tweets with unique user IDs."
      %(len(tweets_w_Location), len(uniqueUsers_w_Location)))

# ---------------------------------------------------------------------------------------------------------------------
# Now take the tweets with both user defined and GPS defined locations and find how far apart they are
#
# Vincenty's formulae
# - Calculates the distance between two points on the surface of a spheroid based on the assumption that the figure
# of the Earth is an oblate spheroid, and hence are more accurate than methods that assume a spherical Earth,
# such as great-circle distance.

geoLats = list(tweets_w_Location['geo_lats'])
geoLons = list(tweets_w_Location['geo_lons'])
usrLats = list(tweets_w_Location['user_lats'])
usrLons = list(tweets_w_Location['user_lons'])

from geopy.distance import vincenty

distance_btw_points = []

for idx in range(0,len(latList)):
    tmpDist = vincenty((latList[idx],lonList[idx]),(usrLats[idx],usrLons[idx])).miles
    distance_btw_points.append(tmpDist)

print("The minimum distance between the user-defined location and the GPS-defined location is %.2f miles"
      %(min(distance_btw_points)))
print("The maximum distance between the user-defined location and the GPS-defined location is %.2f miles"
      %(max(distance_btw_points)))

# Users whos user-defined location and GPS-defined location are within 1 mile of eachother:
distance_btw_points_1 = [i for i in distance_btw_points if i <= 1.0]
print("\nOf the %d users with both user-defined and GPS-defined locations, %d are the same location."
     %(len(tweets_w_Location), len(distance_btw_points_1)))

# Remove all values less than 1 mile:
distance_btw_points_10 = [i for i in distance_btw_points if i > 1.0 and i < 10]
print("\n%d users are between 1 and 10 miles from their user-defined location." %(len(distance_btw_points_10)))

distance_btw_points_100 = [i for i in distance_btw_points if i >= 10 and i < 100]
print("\n%d users are between 10 and 100 miles from their user-defined location." %(len(distance_btw_points_100)))

distance_btw_points_1000 = [i for i in distance_btw_points if i >= 100 and i < 1000]
print("\n%d users are between 100 and 1000 miles from their user-defined location." %(len(distance_btw_points_1000)))

distance_btw_points_big = [i for i in distance_btw_points if i >= 1000]
print("\n%d users are more than 1000 miles from their user-defined location." %(len(distance_btw_points_big)))

# ---------------------------------------------------------------------------------------------------------------------
# Histogram of distance between points:

plt.figure(figsize=(20,20))
plt.rc('xtick', labelsize=25)
plt.rc('ytick', labelsize=25)

plt.subplot(221)
plt.hist(distance_btw_points_10, bins=20)
plt.xlim([1,10])
plt.title("1 to 10 miles", fontsize=25, fontweight='bold')


plt.subplot(222)
plt.hist(distance_btw_points_100)
plt.xlim([10,100])
plt.title("10 to 100 miles", fontsize=25, fontweight='bold')

plt.subplot(223)
plt.hist(distance_btw_points_1000)
plt.xlim([100,1000])
plt.title("100 to 1000 miles", fontsize=25, fontweight='bold')

plt.subplot(224)
plt.hist(distance_btw_points_big)
plt.xlim([1000,11000])
plt.title("Greater than 1000 miles", fontsize=25, fontweight='bold')

plt.show()

# ---------------------------------------------------------------------------------------------------------------------
# Plotting languages
numLang = 10
tweets_by_lang = tweets_full_dataframe['tweet_lang'].value_counts()
tmpLanguages = tweets_by_lang[:numLang]
width = [0.55]
ind = list(range(1,numLang+1))
names = tmpLanguages.keys()

fig, ax = plt.subplots()
rects1 = ax.bar(ind, tmpLanguages, width, color='red')
plt.yscale('log')

ax.set_title('Top 10 languages', fontsize=15, fontweight='bold')
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_xlabel('Languages', fontsize=15)

# Hide the right and top spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Only show ticks on the left and bottom spines
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

ax.set_xticks(ind + width)
ax.set_xticklabels(names)


def autolabel(rects):
    # attach some text labels
    for rect in rects1:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

autolabel(rects1)
plt.show()

# ---------------------------------------------------------------------------------------------------------------------
# Plotting the top 5 languages

tweets_by_lang = tweets_full_dataframe['tweet_lang'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')


# ---------------------------------------------------------------------------------------------------------------------
# Plotting the languages most common, after the 3 top

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('4-10 most common languages', fontsize=15, fontweight='bold')
tweets_by_lang[3:10].plot(ax=ax, kind='bar', color='red')

# ---------------------------------------------------------------------------------------------------------------------
# Map out the tweet location by direct Lat Lon

# Use the Gall–Peters projection
map = Basemap(projection='gall',
              resolution = 'l',
              area_thresh = 100000.0,
              # Centered at 0,0 (i.e null island)
              lat_0=0, lon_0=0)

# Draw the coastlines on the map
map.drawcoastlines()

# Draw country borders on the map
map.drawcountries()

# Fill the land with grey
map.fillcontinents(color = '#888888')

# Draw the map boundaries
map.drawmapboundary(fill_color='#f4f4f4')

# Define longitude and latitude points
x,y = map(tweets_full_dataframe['geo_lons'].values, tweets_full_dataframe['geo_lats'].values)

# Plot using round, red markers, size 6
map.plot(x, y, 'ro', markersize=6)

plt.title('Tweet locations - LatLon encoded directly')

# Show the map
plt.show()

# ---------------------------------------------------------------------------------------------------------------------

# Map out the tweet location by user profile defined Lat Lon

# Use the Gall–Peters projection
map = Basemap(projection='gall',
              resolution = 'l',
              area_thresh = 100000.0,
              # Centered at 0,0 (i.e null island)
              lat_0=0, lon_0=0)

# Draw the coastlines on the map
map.drawcoastlines()

# Draw country borders on the map
map.drawcountries()

# Fill the land with grey
map.fillcontinents(color = '#888888')

# Draw the map boundaries
map.drawmapboundary(fill_color='#f4f4f4')

# Define longitude and latitude points
x,y = map(tweets_full_dataframe['user_lons'].values, tweets_full_dataframe['user_lats'].values)

# Plot using round, red markers, size 6
map.plot(x, y, 'ro', markersize=6)

plt.title('Tweet locations - LatLon from user profile location')

# Show the map
plt.show()