import json
import pandas as pd

# Read in FULL Twitter JSON File:
load_file_name = 'Twitter_Zika_FullData'
with open('../data/%s.json' %(load_file_name), 'r') as twitterJSONFile_in:
    tweets_data_full = json.load(twitterJSONFile_in)

# Use list comprehension to create lists of important information from the JSON file of tweets
# This will be used to populate the pandas data frame

user_ID         = [(T['user']['id'] if 'user' in T else None) for T in tweets_data_full]
user_userName   = [(T['user']['screen_name'] if 'user' in T else None) for T in tweets_data_full]
user_screenName = [(T['user']['name'] if 'user' in T else None) for T in tweets_data_full]
tweet_location  = [(T['place']['full_name'] if 'place' in T and T['place'] is not None else None) for T in tweets_data_full]
tweet_country   = [(T['place']['country_code'] if 'country_code' in T else None) for T in tweets_data_full]
geo_lats        = [(T['geo']['coordinates'][0] if 'geo' in T and T['geo'] is not None else None) for T in tweets_data_full]
geo_lons        = [(T['geo']['coordinates'][1] if 'geo' in T and T['geo'] is not None else None) for T in tweets_data_full]
tweet_time      = [(T['created_at'] if 'created_at' in T else None) for T in tweets_data_full]
tweet_lang      = [(T['lang'] if 'lang' in T and T['lang']!='und' else None) for T in tweets_data_full]
text            = [(T['text'] if 'text' in T else None) for T in tweets_data_full]
in_reply_to_screen_name = [(T['in_reply_to_screen_name'] if 'in_reply_to_screen_name' in T else None) for T in tweets_data_full]

# Determine how many users specify a location in their user profile
tweet_location_names  = [x for x in tweet_location if x is not None]
tweet_location_unique = set(tweet_location_names)
print("%d unique users define their location in their twitter profile." %(len(tweet_location_unique)))

# read in the dictionary of place names and corresponding latitudes & longitudes - JSON file
with open('../data/Twitter_Zika_PlaceName_Geo_info.json', 'r') as tweet_Geo_JSON_File:
    tweet_GeoDict = json.load(tweet_Geo_JSON_File)


# Use the Location_to_LatLon.py script to determine if any of the tweet location names in the variable tweet_location_names
# do not already exist, and if not, convert the location names to latitude and longitude values


# Create two lists: tweet_loc_lats & tweet_loc_lons - each will end up being the length of the full tweet_location list
tweet_loc_lats = []
tweet_loc_lons = []

# Populate the lists with the latitude and longitude values corresponding to the place name in the tweet_location list:
for placeName in tweet_location:
    if placeName is not None:
        tmplat,tmplon = tweet_GeoDict[placeName]
        tweet_loc_lats.append(tmplat)
        tweet_loc_lons.append(tmplon)
    else:
        tweet_loc_lats.append(None)
        tweet_loc_lons.append(None)

# Put all the lists into a Pandas Data Frame:
tweets_full_dataframe = pd.DataFrame({'userID':user_ID, 'userName':user_userName, 'userScreenName':user_screenName,
                                      'tweet_location':tweet_location,'user_lats':tweet_loc_lats,'user_lons':tweet_loc_lons,
                                      'tweet_country':tweet_country, 'geo_lats':geo_lats, 'geo_lons':geo_lons,
                                      'tweet_time':tweet_time, 'tweet_lang':tweet_lang, 'text':text,
                                      'reply_to_ScreenName':in_reply_to_screen_name})

# Print out the last 5 rows of the data frame to ensure it looks as expected
tweets_full_dataframe.tail(5)

