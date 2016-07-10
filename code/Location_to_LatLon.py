import json
from geopy.geocoders import Nominatim

tweet_lat_lon_dict = {}

geolocator = Nominatim()

# Turn the place name into a geo (lat,lon) location

for i, placeName in enumerate(tweet_location_unique):
    if placeName not in tweet_lat_lon_dict:
        try:
            placeGeo  = geolocator.geocode(placeName)
        except Exception as E:
            print("exception happened", type(E), E)

        if i % 20 == 0:
            print(i)
        if placeGeo is not None:
            tweet_lat_lon_dict[placeName] = (placeGeo.latitude, placeGeo.longitude)
        else:
            tweet_lat_lon_dict[placeName] = (None, None)

print(len(tweet_lat_lon_dict))
bad_place_names = [k for k,v in tweet_lat_lon_dict.items() if v == (None,None)]
print(len(bad_place_names))
print("\n".join(bad_place_names))

# Write out the dictionary of place names and corresponding latitutes & longitudes to a JSON file
with open('../data/Twitter_Zika_PlaceName_Geo_info.json', 'w') as twitterGeo_JSONFile:
    json.dump(tweet_lat_lon_dict, twitterGeo_JSONFile, indent=2)

