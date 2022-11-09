from geopy.distance import geodesic


def get_distance_from_two_locations(location1, location2):
    """
    returns the distance in km
    location is a string in the format of "lat,lng"
    """

    lat1, lng1 = location1.split(",")
    lat2, lng2 = location2.split(",")
    return geodesic((lat1, lng1), (lat2, lng2)).km
