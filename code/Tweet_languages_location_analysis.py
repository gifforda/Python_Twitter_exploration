import re
import json
import pandas as pd
import matplotlib
matplotlib.use('nbAgg')
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim

# Finding unique values

uniqueID       = tweets_full_dataframe.userID.unique()
uniqueLocation = tweets_full_dataframe.tweet_location.unique()
uniqueLanguage = tweets_full_dataframe.tweet_lang.unique()

print("There are %d tweets in this dataframe, but only %d unique users." %(len(tweets_full_dataframe), len(uniqueID)))
print("Of the %d unique users, there are %d different languages represented." %(len(uniqueID), len(uniqueLanguage)))
print("Of the %d unique users, %d listed a self-reported location." %(len(uniqueID), len(uniqueLocation)))

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
x,y = map(tweets_full_dataframe['user_lons'].values, tweets_full_dataframe['user_lats'].values)

# Plot using round, red markers, size 6
map.plot(x, y, 'ro', markersize=6)

plt.title('Tweet locations - LatLon from user profile location')

# Show the map
plt.show()