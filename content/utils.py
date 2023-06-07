from geopy.distance import geodesic


def get_distance_from_two_coordinates(coordinates1, coordinates2):
    try:
        return geodesic(
            (coordinates1["latitude"], coordinates1["longitude"]),
            (coordinates2["latitude"], coordinates2["longitude"])
        ).meters
    except:
        return 0
