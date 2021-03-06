'''
This code:
- reads in the .JSON file generated by Load_Data.py
- uses list comprehension to extract important information from the JSON file for each tweet, if the information
    exists for that tweet
- determines how many users specify their location in their user profile, and of these, how many are unique locations
- this list of unique locations is then turned into a dictionary of {key: value} pairs,
    where the place name is the key, and the (lat, lon) tuple is the value.

'''

import json
import os.path
import pandas as pd
from Location_to_LatLon import make_LatLonDict

# Read in FULL Twitter JSON File:
load_file_name = input('Enter the output JSON file name (excluding file type ending):  ')
with open('../data/%s.json' %(load_file_name), 'r') as twitterJSONFile_in:
    tweets_data_full = json.load(twitterJSONFile_in)

# Use list comprehension to create lists of important information from the JSON file of tweets
# This will be used to populate the pandas data frame

user_ID = [(T['user']['id'] if 'user' in T else None) for T in tweets_data_full]
user_userName = [(T['user']['screen_name'] if 'user' in T else None) for T in tweets_data_full]
user_screenName = [(T['user']['name'] if 'user' in T else None) for T in tweets_data_full]
user_def_location = [(T['place']['full_name'] if 'place' in T and T['place'] is not None else None) for T in tweets_data_full]
user_def_country = [(T['place']['country_code'] if 'country_code' in T else None) for T in tweets_data_full]
gps_lats = [(T['geo']['coordinates'][0] if 'geo' in T and T['geo'] is not None else None) for T in tweets_data_full]
gps_lons = [(T['geo']['coordinates'][1] if 'geo' in T and T['geo'] is not None else None) for T in tweets_data_full]
tweet_time = [(T['created_at'] if 'created_at' in T else None) for T in tweets_data_full]
tweet_lang = [(T['lang'] if 'lang' in T and T['lang']!='und' else None) for T in tweets_data_full]
text = [(T['text'] if 'text' in T else None) for T in tweets_data_full]
in_reply_to_screen_name = [(T['in_reply_to_screen_name'] if 'in_reply_to_screen_name' in T else None) for T in tweets_data_full]

# Determine how many users specify a location in their user profile, and how many are unique locations
tweet_location_names = [x for x in user_def_location if x is not None]
tweet_location_unique = set(tweet_location_names)
print("%d unique users define their location in their twitter profile." %(len(tweet_location_unique)))

# Use the Location_to_LatLon.py script to determine if any of the tweet location names in the variable tweet_location_names
# do not already exist, and if not, convert the location names to latitude and longitude values
# NOTE:
#   - If it is the first time, and the (lat, lon) dictionary has not yet been created, run Location_to_LatLon.py to create the dictionary
# Otherwise:
#   - read in the (lat, lon) dictionary previously created, and run Location_to_LatLon.py on the new list of
#   locations to add any new locations to the (lat, lon) dictionary, and save out the new (potentially enhanced) (lat, lon) dictionary.

# if the (lat, lon) dictionary file does not exist
if os.path.isfile('../data/Twitter_Zika_PlaceName_Geo_info.json') == False:
    tweet_GeoDict = {}
else:
    # read in the previously created dictionary of place names and corresponding latitudes & longitudes - JSON file
    with open('../data/Twitter_Zika_PlaceName_Geo_info.json', 'r') as tweet_Geo_JSON_File:
        tweet_GeoDict = json.load(tweet_Geo_JSON_File)

# call the make_LatLonDict module in Location_to_LatLon.py to populate the (lat, lon) dictionary,
#   either for the first time, or with the new unique location names
make_LatLonDict(tweet_GeoDict, tweet_location_unique)

# Create two lists: user_def_lats & user_def_lons - each will end up being the length of the full tweet_location list
user_def_lats = []
user_def_lons = []

# Populate the lists with the latitude and longitude values corresponding to the place name in the tweet_location list:
for placeName in user_def_location:
    if placeName is not None:
        tmplat, tmplon = tweet_GeoDict[placeName]
        user_def_lats.append(tmplat)
        user_def_lons.append(tmplon)
    else:
        user_def_lats.append(None)
        user_def_lons.append(None)

# Put all the lists into a Pandas Data Frame:
tweets_full_dataframe = pd.DataFrame({'userID':user_ID, 'userName':user_userName, 'userScreenName':user_screenName,
                                      'user_defined_location':user_def_location,'user_lats':user_def_lats,'user_lons':user_def_lons,
                                      'user_defined_country':user_def_country, 'gps_lats':gps_lats, 'gps_lons':gps_lons,
                                      'tweet_time':tweet_time, 'tweet_lang':tweet_lang, 'text':text,
                                      'in_reply_to_ScreenName':in_reply_to_screen_name})

# Print out the last 5 rows of the data frame to ensure it looks as expected
print(tweets_full_dataframe.tail(5))

# Save the data Frame for use:
tweets_full_dataframe.to_pickle('../data/Tweets_Full_Data_Frame.pkl')