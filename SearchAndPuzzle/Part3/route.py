#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Abhiroop Tejomay Kommalapati (akommala), Divya Jagabattula (djagabat), Chiranthan Shadaksharaswamy (cshadaks)
#
# Based on skeleton code by V. Mathur and D. Crandall, Fall 2022
#


# !/usr/bin/env python3
from operator import delitem
import sys
import math

def load_city_gps(path):
    output = {}
    with open(path, 'r') as f:
        for line in f.readlines():
            city, lat, long = line.split(' ')
            output.update(
                {
                    city: (float(lat), float(long[:-1]))
                }
            )

    return output


def load_road_segments(path):
    output = []
    with open(path, 'r') as f:
        for line in f.readlines():
            start_city, end_city, distance, speed_limit, highway = line.split(' ')
            output.append(
                (
                    start_city,
                    end_city,
                    distance, 
                    speed_limit,
                    highway[:-1]
                )
            )

    return output
       
def successors(state, road_segments):
    s = []
    for start_city, end_city, distance, speed_limit, highway in road_segments:
        destination = None
        if state == start_city:
            destination = end_city
        if state == end_city:
            destination = start_city
        if destination is not None:
            s.append([destination, int(distance), int(speed_limit), highway])
    return s

def is_goal(city, destination):
    return city == destination

def h(lat1, long1, lat2, long2, cost, highest_speed_limit, longest_road):
    # https://en.wikipedia.org/wiki/Haversine_formula
    def haversine(lat1, long1, lat2, long2):
        phi1 = lat1 * (math.pi / 180)
        phi2 = lat2 * (math.pi / 180)
        lambda1 = long1 * (math.pi / 180)
        lambda2 = long2 * (math.pi / 180)
        radius_of_earth = 3958.8

        return 2 * radius_of_earth * math.asin(
            math.sqrt(
                (math.sin((phi2 - phi1) / 2) ** 2) + 
                (math.cos(phi1) * math.cos(phi2) * math.sin((lambda2 - lambda1) / 2) ** 2)
            )
        )
    
    if cost == 'distance':
        return haversine(lat1, long1, lat2, long2) - 20
    elif cost == 'time' or cost == 'delivery':
        return haversine(lat1, long1, lat2, long2) / highest_speed_limit
    elif cost == 'segments':
        return haversine(lat1, long1, lat2, long2) / longest_road
    else:
        return ValueError(f'Invalid cost {cost}, cost should one of `distance`, `time`, `segments` or `delivery`.')

def get_route(start, end, cost):
    
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    city_gps = load_city_gps('./city-gps.txt')
    road_segments = load_road_segments('./road-segments.txt')
    longest_road, highest_speed_limit = int(road_segments[0][2]), int(road_segments[0][3])
    for _, _, distance, speed_limit, _ in road_segments:
        if int(distance) > longest_road:
            longest_road = int(distance)
        if int(speed_limit) > highest_speed_limit:
            highest_speed_limit = int(speed_limit)

    if city_gps.get(start, False) and city_gps.get(end, False):
        start_lat, start_long = city_gps[start]
        end_lat, end_long = city_gps[end]
        init_cost = h(start_lat, start_long, end_lat, end_long, cost, highest_speed_limit, longest_road)
    elif not city_gps.get(start, False) and city_gps.get(end, False):
        init_cost = 0
        end_lat, end_long = city_gps[end]
    elif city_gps.get(start, False) and not city_gps.get(end, False):
        init_cost = 99999
        start_lat, start_long = city_gps[start]
        for city, distance, speed_limit, highway in successors(end, road_segments):
            if city_gps.get(city, False):
                lat, long = city_gps[city]
                if h(start_lat, start_long, end_lat, end_long, cost, highest_speed_limit, longest_road) < init_cost:
                    init_cost = h(start_lat, start_long, lat, long, cost, highest_speed_limit, longest_road)
                    end_lat, end_long = lat, long
    else:
        init_cost = 99999
        for start_city, start_distance, start_speed_limit, start_highway in successors(start, road_segments):
            if city_gps.get(start_city, False):
                for end_city, end_distance, end_speed_limit, end_highway in successors(end, road_segments):
                    if city_gps(end_city, False):
                        start_lat, start_long = city_gps[start_city]
                        lat, long = city_gps[end_city]
                        if h(start_lat, start_long, end_lat, end_long, cost, highest_speed_limit, longest_road) < init_cost:
                            init_cost = h(start_lat, start_long, lat, long)
                            end_lat, end_long = lat, long

    fringe = [(0, start, 0, 1, '', 0, 0, []), ]
    reached = [start]
    reached_costs = [0]

    if is_goal(start, end):
        return((0, 0, 0, [(start, '' + ' for ' + str(0) + ' miles')]))

    while len(fringe) > 0:
        fringe.sort(reverse=True)
        _, city, distance, speed_limit, highway, time, delivery_time, path = fringe.pop()

        if is_goal(city, end):
            return {
                'total-segments': len(path),
                'total-miles': float(distance),
                'total-hours': float(time), 
                'total-delivery-hours': float(delivery_time), 
                'route-taken': path
            }

        for s_city, s_distance, s_speed_limit, s_highway in successors(city, road_segments):
            if s_speed_limit >= 50:
                p_of_fall_out = math.tanh(s_distance / 1000)
            else:
                p_of_fall_out = 0

            t_road = s_distance / s_speed_limit
            t_trip = delivery_time
            additional_delivery_time = t_road + (2 * p_of_fall_out * (t_road + t_trip))
            
            if cost == 'distance':
                if city_gps.get(city, False):
                    lat, long = city_gps[city]
                    s_cost = h(lat, long, end_lat, end_long, cost, highest_speed_limit, longest_road) + (distance + s_distance)
                else:
                    s_cost = distance + s_distance

                if s_city not in reached:
                    reached.append(s_city)
                    reached_costs.append(s_cost)

                    fringe.append(
                        (
                            s_cost,
                            s_city,
                            distance + s_distance,
                            s_speed_limit,
                            s_highway,
                            time + (int(s_distance) / int(s_speed_limit)),
                            delivery_time + additional_delivery_time,
                            path + [(s_city, f'{s_highway} for {s_distance} miles')]
                        )
                    )

                elif s_city in reached and s_cost < reached_costs[reached.index(s_city)]:
                    reached.pop(reached.index(s_city))     
                    reached.append(s_city)
                    reached_costs.append(s_cost)
                    fringe.append(
                        (
                            s_cost,
                            s_city,
                            distance + s_distance,
                            s_speed_limit,
                            s_highway,
                            time + (int(s_distance) / int(s_speed_limit)),
                            delivery_time + additional_delivery_time,
                            path + [(s_city, f'{s_highway} for {s_distance} miles')]
                        )
                    )


            elif cost == 'time':
                if city_gps.get(city, False):
                    lat, long = city_gps[city]
                    s_cost = h(lat, long, end_lat, end_long, cost, highest_speed_limit, longest_road) + (time + (int(s_distance) / int(s_speed_limit)))
                else:
                    s_cost = time + int(s_distance)

                if s_city not in reached:
                    reached.append(s_city)
                    reached_costs.append(s_cost)

                    fringe.append(
                        (
                            s_cost,
                            s_city,
                            distance + s_distance,
                            s_speed_limit,
                            s_highway,
                            time + (int(s_distance) / int(s_speed_limit)),
                            delivery_time + additional_delivery_time,
                            path + [(s_city, f'{s_highway} for {s_distance} miles')]
                        )
                    )

                elif s_city in reached and s_cost < reached_costs[reached.index(s_city)]:
                    reached.pop(reached.index(s_city))     
                    reached.append(s_city)
                    reached_costs.append(s_cost)
                    fringe.append(
                        (
                            s_cost,
                            s_city,
                            distance + s_distance,
                            s_speed_limit,
                            s_highway,
                            time + (int(s_distance) / int(s_speed_limit)),
                            delivery_time + additional_delivery_time,
                            path + [(s_city, f'{s_highway} for {s_distance} miles')]
                        )
                    )

            elif cost == 'segments':
                if city_gps.get(city, False):
                    lat, long = city_gps[city]
                    s_cost = h(lat, long, end_lat, end_long, cost, highest_speed_limit, longest_road) + len(path) + 1
                else:
                    s_cost = 1

                if s_city not in reached:
                    reached.append(s_city)
                    reached_costs.append(s_cost)

                    fringe.append(
                        (
                            s_cost,
                            s_city,
                            distance + s_distance,
                            s_speed_limit,
                            s_highway,
                            time + (int(s_distance) / int(s_speed_limit)),
                            delivery_time + additional_delivery_time,
                            path + [(s_city, f'{s_highway} for {s_distance} miles')]
                        )
                    )

                elif s_city in reached and s_cost < reached_costs[reached.index(s_city)]:
                    reached.pop(reached.index(s_city))     
                    reached.append(s_city)
                    reached_costs.append(s_cost)
                    fringe.append(
                        (
                            s_cost,
                            s_city,
                            distance + s_distance,
                            s_speed_limit,
                            s_highway,
                            time + (int(s_distance) / int(s_speed_limit)),
                            delivery_time + additional_delivery_time,
                            path + [(s_city, f'{s_highway} for {s_distance} miles')]
                        )
                    )

            elif cost == 'delivery':
                if city_gps.get(city, False):
                    lat, long = city_gps[city]
                    s_cost = h(lat, long, end_lat, end_long, cost, highest_speed_limit, longest_road) + delivery_time + additional_delivery_time
                else:
                    s_cost = delivery_time + additional_delivery_time + 1

                if s_city not in reached:
                    reached.append(s_city)
                    reached_costs.append(s_cost)
                    
                    fringe.append(
                        (
                            s_cost,
                            s_city,
                            distance + s_distance,
                            s_speed_limit,
                            s_highway,
                            time + (int(s_distance) / int(s_speed_limit)),
                            delivery_time + additional_delivery_time,
                            path + [(s_city, f'{s_highway} for {s_distance} miles')]
                        )
                    )

                elif s_city in reached and s_cost < reached_costs[reached.index(s_city)]:
                    reached.pop(reached.index(s_city))     
                    reached.append(s_city)
                    reached_costs.append(s_cost)

                    fringe.append(
                        (
                            s_cost,
                            s_city,
                            distance + s_distance,
                            s_speed_limit,
                            s_highway,
                            time + (int(s_distance) / int(s_speed_limit)),
                            delivery_time + additional_delivery_time,
                            path + [(s_city, f'{s_highway} for {s_distance} miles')]
                        )
                    )

    return f'Path {start} to {end} not found!'


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])


