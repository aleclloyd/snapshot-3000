import requests
import math
import click

# 1. get data
meteor_resp = requests.get('https://data.nasa.gov/resource/y77d-th95.json')
# 2. convert to pyt data struc
meteor_data = meteor_resp.json()


@click.command()
@click.option('--latitude', default=None, help='Current Latitude (tag Lat:<name>)')
@click.option('--longitude', default=None, help='Current Longitude (tag Long:<name>)')
def meteor_distance(latitude, longitude):

    if latitude:
        # my_loc = {latitude,longitude}
        for meteor in meteor_data:
            if not ('reclat' in meteor and 'reclong' in meteor): continue
            # meteor['distance'] = calc_dist(float(meteor['reclat']), float(meteor['reclong']), my_loc[0], my_loc[1])
            meteor['distance'] = calc_dist(float(meteor['reclat']), float(meteor['reclong']), \
                                           float(latitude), float(longitude))
            # print(meteor)
            # print(",".join(("Name: " + meteor['name'], "Distance: " + str(meteor['distance']), "Mass: " + meteor['mass'])))
            # print(",".join(
            #     ("Name: " + meteor['name'], "Distance: " + str(meteor['distance']))))

    else:
        print("No values entered")

    # meteor_data.sort(key=get_dist)
    print(meteor_data[0:10])
    print("done")
    return
    # meteor_data.sort(key=get_dist)
    # i = 0
    # for m in meteor_data:
    #     i +=int(1)
    #     if i < 11:
    #         # print(m)
    #         # return
    #         if
    #         print(",".join(("Name: " + m['name'], "Distance: "+ str(m['distance']), "Mass: " + m['mass'])))


# 3 calc distance between landing structure and current location
def calc_dist(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    h = math.sin( (lat2 - lat1) / 2 ) ** 2 + \
        math.cos(lat1) * \
        math.cos(lat2) * \
        math.sin( (lon2 - lon1) / 2 ) ** 2
    # print("here")
    return 6372.8 * 2 * math.asin(math.sqrt(h))


# 4. sort by distance
def get_dist(meteor):
    return meteor.get('distance',math.inf)


if __name__ == '__main__':
    meteor_distance()


# meteor_data.sort(key=get_dist)


# 5. slect 1o closest sites and print
# meteor_data[0:10]
# all items where there is no  location information
# len([m for m in meteor_data if 'distance' not in m])

#
# def calc_dist(lat1,lon1,lat2,lon2):
#     lat1 = math.radians(lat1)
#     lon1 = math.radians(lon1)
#     lat2 = math.radians(lat2)
#     lon2 = math.radians(lon2)
#     h = math.sin( (lat2 - lat1) / 2 ** 2 + \
#     math.cos(lat1)* \
#     math.cos(lat2)* \
#     math.sin((lon2-lon1)/2) ** 2
#     return 6372.8*2* math.asin(math.sqrt(h))
