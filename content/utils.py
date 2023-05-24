from geopy.distance import geodesic


def get_distance_from_two_coordinatess(coordinates1, coordinates2):
    """
    returns the distance in km
    coordinates is a string in the format of "lat,lng"
    """

    lat1, lng1 = coordinates1.split(",")
    lat2, lng2 = coordinates2.split(",")
    return geodesic((lat1, lng1), (lat2, lng2)).km
