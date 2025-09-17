# skyroute.py is where to build the SkyRoute tool
from graph_search import bfs, dfs
from vc_metro import vc_metro
from vc_landmarks import vc_landmarks
from landmark_choices import landmark_choices

# Task 0: landmarks string
landmark_string = "\n".join([f"{letter} - {name}" for letter, name in landmark_choices.items()])

# Task 1-2: greet function
def greet():
    print("Hi there and welcome to SkyRoute!")
    print("We'll help you find the shortest route between the following Vancouver landmarks:\n" + landmark_string)

# Task 3: main program wrapper
def skyroute():
    greet()
    new_route()
    goodbye()

# Task 4-11: handle start and end points
def get_start():
    start_point_letter = input("Where are you coming from? Type in the corresponding letter: ")
    if start_point_letter in landmark_choices:
        return landmark_choices[start_point_letter]
    else:
        print("Sorry, that's not a landmark we have data on. Let's try this again...")
        return get_start()

def get_end():
    end_point_letter = input("Ok, where are you headed? Type in the corresponding letter: ")
    if end_point_letter in landmark_choices:
        return landmark_choices[end_point_letter]
    else:
        print("Sorry, that's not a landmark we have data on. Let's try this again...")
        return get_end()

def set_start_and_end(start_point=None, end_point=None):
    if start_point:
        change_point = input(
            "What would you like to change? You can enter 'o' for 'origin', 'd' for 'destination', or 'b' for 'both': "
        )
        if change_point == "b":
            start_point = get_start()
            end_point = get_end()
        elif change_point == "o":
            start_point = get_start()
        elif change_point == "d":
            end_point = get_end()
        else:
            print("Oops, that isn't 'o', 'd', or 'b'...")
            return set_start_and_end(start_point, end_point)
    else:
        start_point = get_start()
        end_point = get_end()
    return start_point, end_point

# Task 15-22: get shortest route
def get_route(start_point, end_point):
    start_stations = vc_landmarks[start_point]
    end_stations = vc_landmarks[end_point]
    routes = []

    for start_station in start_stations:
        for end_station in end_stations:
            route = bfs(vc_metro, start_station, end_station)
            if route:
                routes.append(route)

    if routes:
        shortest_route = min(routes, key=len)
        return shortest_route
    return None

# Task 13-33: new_route function + looping
stations_under_construction = []

def new_route(start_point=None, end_point=None):
    start_point, end_point = set_start_and_end(start_point, end_point)
    
    shortest_route = get_route(start_point, end_point)
    
    if shortest_route:
        shortest_route_string = "\n".join(shortest_route)
        print(f"The shortest metro route from {start_point} to {end_point} is:\n{shortest_route_string}")
    else:
        print(f"Unfortunately, there is currently no path between {start_point} and {end_point} due to maintenance.")
    
    again = input("Would you like to see another route? Enter y/n: ")
    if again.lower() == "y":
        show_landmarks()
        new_route(start_point, end_point)

def show_landmarks():
    see_landmarks = input("Would you like to see the list of landmarks again? Enter y/n: ")
    if see_landmarks.lower() == "y":
        print(landmark_string)

def goodbye():
    print("Thanks for using SkyRoute!")

# Task 38-43: handle stations under construction
def get_active_stations():
    updated_metro = {station: set(neighbors) for station, neighbors in vc_metro.items()}
    for station_under_construction in stations_under_construction:
        for station, neighbors in vc_metro.items():
            if station != station_under_construction:
                updated_metro[station] = neighbors - set(stations_under_construction)
            else:
                updated_metro[station] = set()
    return updated_metro

# Task 44-49: adapt get_route to handle stations under construction
def get_route(start_point, end_point):
    start_stations = vc_landmarks[start_point]
    end_stations = vc_landmarks[end_point]
    routes = []

    for start_station in start_stations:
        for end_station in end_stations:
            metro_system = get_active_stations() if stations_under_construction else vc_metro
            if stations_under_construction:
                possible_route = dfs(metro_system, start_station, end_station)
                if not possible_route:
                    continue
            route = bfs(metro_system, start_station, end_station)
            if route:
                routes.append(route)

    if routes:
        shortest_route = min(routes, key=len)
        return shortest_route
    return None

# Task 50: call skyroute() to run
if __name__ == "__main__":
    skyroute()
