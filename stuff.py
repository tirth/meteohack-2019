import logging
from ac_calc import data, geocode_api, climate_api


def go():
    print('yo')

    # data.read_ac_usage()

    cap, eer = data.ac_values('LW5015E')
    print(cap, eer)

    lat, long = geocode_api.get_lat_long('Toronto, ON')

    close_stations = climate_api.stations_by_proximity(lat, long)

    for station in close_stations[2:3]:
        print(station)

        climate_api.station_dates(station[0])

        for m in range(1, 13):
            temp_data, precip_data = climate_api.get_hourly_data(station[0], 2018, m)
            print(temp_data)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    go()
