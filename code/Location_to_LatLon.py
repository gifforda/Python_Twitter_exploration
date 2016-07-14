import json
from geopy.geocoders import Nominatim

def make_LatLonDict(tweet_lat_lon_dict, tweet_location_unique):

    geolocator = Nominatim()

    # Turn the user defined location place name into a geographic (lat,lon) location

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


    # How many location place names were not able to be turned into (lat,lon) locations?
    # Which names were they?
    print("The total (lat,lon) dictionary is %d items long." %(len(tweet_lat_lon_dict)))

    bad_place_names = [k for k,v in tweet_lat_lon_dict.items() if v == (None,None)]

    print("Of these, %d were unable to be converted into (lat,lon) coordinates. These were specifically the following locations: \n" %(len(bad_place_names)))
    print("\n".join(bad_place_names))

    # Write out the dictionary of place names and corresponding latitutes & longitudes to a JSON file
    with open('../data/Twitter_Zika_PlaceName_Geo_info.json', 'w') as twitterGeo_JSONFile:
        json.dump(tweet_lat_lon_dict, twitterGeo_JSONFile, indent=2)
