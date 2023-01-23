"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Student Id: 0123456
Name:       Xxxx Yyyyyy
Email:      xxxx.yyyyyy@tuni.fi

Project 3: ...
"""


def find_route(data, departure, destination):
    """
    This function tries to find a route between <departure>
    and <destination> cities. It assumes the existence of
    the two functions fetch_neighbours and distance_to_neighbour
    (see the assignment and the function templates below).
    They are used to get the relevant information from the data
    structure <data> for find_route to be able to do the search.

    The return value is a list of cities one must travel through
    to get from <departure> to <destination>. If for any
    reason the route does not exist, the return value is
    an empty list [].

    :param data: ?????, A data structure of an unspecified type (you decide)
           which contains the distance information between the cities.
    :param departure: str, the name of the departure city.
    :param destination: str, the name of the destination city.
    :return: list[str], a list of cities the route travels through, or
           an empty list if the route can not be found. If the departure
           and the destination cities are the same, the function returns
           a two element list where the departure city is stored twice.
    """

    # +--------------------------------------+
    # |                                      |
    # |     DO NOT MODIFY THIS FUNCTION!     |
    # |                                      |
    # +--------------------------------------+

    if departure not in data:
        return []

    elif departure == destination:
        return [departure, destination]

    greens = {departure}
    deltas = {departure: 0}
    came_from = {departure: None}

    while True:
        if destination in greens:
            break

        red_neighbours = []
        for city in greens:
            for neighbour in fetch_neighbours(data, city):
                if neighbour not in greens:
                    delta = deltas[city] + distance_to_neighbour(data, city,
                                                                 neighbour)
                    red_neighbours.append((city, neighbour, delta))

        if not red_neighbours:
            return []

        current_city, next_city, delta = min(red_neighbours, key=lambda x: x[2])

        greens.add(next_city)
        deltas[next_city] = delta
        came_from[next_city] = current_city

    route = []
    while True:
        route.append(destination)
        if destination == departure:
            break
        destination = came_from.get(destination)

    return list(reversed(route))


def read_distance_file(file_name):
    """
    Reads the distance information from <file_name> and stores it
    in a suitable data structure (you decide what kind of data
    structure to use). This data structure is also the return value,
    unless an error happens during the file reading operation.

    :param file_name: str, The name of the file to be read.
    :return: dict_file_contents | None: A data structure containing the
             information read from the <file_name> or None if any kind of error
             happens. The data structure to be chosen is completely up to you as
             long as all the required operations can be implemented using it.
    """

    dict_file_contents = {}

    try:
        # UTF-8 mahdollistaa "ääkkösten" käsittelyn
        text_file = open(file_name, mode="r", encoding="utf-8")

        # Lukee tiedoston sisällön riveittäin, kerää halutut tiedot talteen
        # omiin kenttiin ja laittaa arvoja sanakirjaan niin, että hakuavaimeksi
        # tulee rivin ensimmäinen kenttä eli haettava kaupunki.
        for line in text_file:
            line = line.strip()

            # Rivin kentät otetaan talteen omiin muuttujiinsa
            departure, destination, distance = line.split(";")

            add_routes_to_dict(departure, destination, distance,
                               dict_file_contents)

        text_file.close()

    # Tiedoston luku epäonnistuu
    except OSError:
        return None

    # Rivi ei noudata haluttua muotoilua (lähtökaupunki;kohdekaupunki;etäisyys)
    except ValueError:
        return None

    return dict_file_contents


def fetch_neighbours(data, city):
    """
    Returns a list of all the cities that are directly
    connected to parameter <city>. In other words, a list
    of cities where there exist an arrow from <city> to
    each element of the returned list. Return value is
    an empty list [], if <city> is unknown or if there are no
    arrows leaving from <city>.

    :param data: ?????, A data structure containing the distance
           information between the known cities.
    :param city: str, the name of the city whose neighbours we
           are interested in.
    :return: list[str], the neighbouring city names in a list.
             Returns [], if <city> is unknown (i.e. not stored as
             a departure city in <data>) or if there are no
             arrows leaving from the <city>.
    """

    list_neighbouring_cities = []

    # Jos lähtökaupunkia ei löydy sanakirjasta
    # if city not in data:
    #     print(f"Error: '{city}' is unknown.")
    #     return

    # Hankitaan sisäkkäisillä silmukoilla kohdekaupungit sanakirjasta
    # ja lisätään ne listalle, joka palautetaan kutsufunktiolle.
    for key_departures, payload_destinations in sorted(data.items()):

        if key_departures == city:
            for key_destinations, payload_distance in \
                    sorted(payload_destinations.items()):
                list_neighbouring_cities.append(key_destinations)

    return list_neighbouring_cities


def distance_to_neighbour(data, departure, destination):
    """
    Returns the distance between two neighbouring cities.
    Returns None if there is no direct connection from
    <departure> city to <destination> city. In other words
    if there is no arrow leading from <departure> city to
    <destination> city.

    :param data: ?????, A data structure containing the distance
           information between the known cities.
    :param departure: str, the name of the departure city.
    :param destination: str, the name of the destination city.
    :return: int | None, The distance between <departure> and
           <destination>. None if there is no direct connection
           between the two cities.
    """

    # if {departure: destination} not in data.items():
    #     return 0


    str_distance = data[departure][destination]
    int_distance = int(str_distance)

    return int_distance

    # {key_departures: {key_destinations: payload_distance}}
    #                            payload_destinations




    # for key_departures, payload_destinations in sorted(data.items()):
    #     if key_departures == departure:
    #     for key_destinations, payload_distance in \
    #             sorted(payload_destinations.items()):
    #         if key_destinations == destination:
    #


def display_routes(dict_routes, city=""):
    """
    LISÄÄÄ TÄHÄN JOTAIN HAUSKAA!!!
    :param dict_routes:
    :return:
    """

    # MUUTTUJIEN ALUSTUKSET TIETOTYYPEITTÄIN AAKKOSJÄRJESTYKSESSÄ

    # Kokonaisluvut
    len_original_space_of_str_departures = 14
    len_original_space_of_str_destinations = 14
    len_original_space_of_str_distance = 5
    len_str_departures_with_spaces = 0

    # Merkkijonot
    str_payload_distance = ""

    #
    for key_departures, payload_destinations in sorted(dict_routes.items()):

        for key_destinations, payload_distance in \
                sorted(payload_destinations.items()):
            leftover_space_of_departures = \
                len_original_space_of_str_departures - len(key_departures)

            leftover_space_of_destinations = \
                len_original_space_of_str_destinations - len(
                    key_destinations)

            str_payload_distance = str(payload_distance)
            leftover_space_of_distance = \
                len_original_space_of_str_distance - len(
                    str_payload_distance)

            len_str_destinations_with_spaces = key_destinations + " " * \
                                               leftover_space_of_destinations
            len_str_distance_with_spaces = " " * leftover_space_of_distance + \
                                           str_payload_distance

            # Jos lähtökaupunkia ei ole syötetty, tallennetaan reittien tiedot
            # muuttujiin ja tulostetaan ne print_routes funktiossa.
            if city == "":

                len_str_departures_with_spaces = key_departures + " " * \
                                                 leftover_space_of_departures
                route_display(len_str_departures_with_spaces,
                              len_str_destinations_with_spaces,
                              len_str_distance_with_spaces)

            # Jos lähtökaupunki syötetään, tallennetaan lähtökaupungin tiedot
            # omaan muuttujaan ja tulostetaan lähtökaupunki ja sen
            # naapurikaupungit print_routes funktiossa.
            elif key_departures == city:
                len_str_city_with_spaces = city + " " * \
                                           leftover_space_of_departures

                route_display(len_str_city_with_spaces,
                              len_str_destinations_with_spaces,
                              len_str_distance_with_spaces)


def route_display(departure, destinations, distance):
    """
    jotaon hasua
    :param departure:
    :param destinations:
    :param distance:
    :return:
    """

    print(departure + destinations + distance)


def add_routes_to_dict(departure, destination, distance, dict_routes):
    """
    fdsaf
    :param departure:
    :param destination:
    :param distance:
    :param dict_routes:
    :return:
    """
    # Jos rivillä olevaa kaupunkia ei löydy sanakirjasta, luodaan
    # sanakirjaan kokonaan uusi avain lähtökaupungin nimellä
    if departure not in dict_routes:
        dict_routes[departure] = {destination: distance}

    # Jos lähtökaupunki löytyy jo sanakirjasta, päivitetään vain sieltä
    # lähteviä reittejä
    else:
        dict_routes[departure][destination] = distance


def ask_for_a_route(dict_routes):
    """
    LISÄÄ TÄHÄN JOTAIN HAUSKAA!!
    :param dict_routes:
    :return:
    """

    # MUUTTUJIEN ALUSTUKSET TIETOTYYPEITTÄIN AAKKOSJÄRJESTYKSESSÄ

    # Kokonaisluvut
    distance_between_cities = 0

    # Merkkijonot
    departure_city = ""
    destination_city = ""
    str_distance_between_cities = ""

    # Kaupunkien nimien alkukirjaimet muutetaan isoiksi, jos ne eivät sitä ole.
    # Tämä siksi, että tulostaminen aakkosjärjestyksessä display-funktiossa
    # toimisi oikein.
    departure_city = input("Enter departure city: ").title()
    destination_city = input("Enter destination city: ").title()
    str_distance_between_cities = input("Distance: ")

    # Etäisyys yritetään muuttaa kokonaisluvuksi.
    try:
        distance_between_cities = int(str_distance_between_cities)

    # Jos kokonaisluvuksi muuttaminen ei onnistu, tulostuu virheilmoitus.
    except ValueError:
        print(f"Error: '{str_distance_between_cities}' is not an integer.")
        return None

    add_routes_to_dict(departure_city, destination_city,
                       distance_between_cities, dict_routes)


def remove_route(dict_routes):
    """
    LISÄÄ TÄHÄN JOTAIN HAUSKAA
    :param dict_routes:
    :return:
    """

    # Käytetään string.title metodia aakkosjärjestyksen varmistamiseksi.
    # Ilman tätä järjestäisi isot ja pienet kirjaimet "omiksi listoikseen"
    # sorted:illa, ts. menetettäisiin oikea aakkosjärjestys.
    departure_city = input("Enter departure city: ").title()

    # Jos lähtökaupunkia ei löydy sanakirjasta, ei kysytä kohdekaupunkia vaan
    # tulsotetaan suoraan error.
    if departure_city not in dict_routes:
        print(f"Error: '{departure_city}' is unknown.")
        return

    # Jos lähtökaupunki löytyi, kysytään kohdekaupunki.
    destination_city = input("Enter destination city: ").title()

    # Jos kohdekaupunkia ei ole sanakirjan hakuavaimessa eli lähtökaupungilla
    # ei ole syötettyä kohdekaupunkia, tulostetaan error.
    if destination_city not in dict_routes[departure_city]:
        print(f"Error: missing road segment between '{departure_city}' and "
              f"'{destination_city}'.")
        return

    # Jos sekä lähtö- että kohdekaupunki löytyvät, poistetaan niiden välinen
    # reitti eli hakuavaimen ja hyötykuorman muodostama pari sanakirjasta.
    del dict_routes[departure_city][destination_city]


def calculate_route_distance(dict_routes, list_route):
    """
    fsfdsa
    :param dict_routes:
    :param list_route:
    :return:
    """
    #

    # route_distance = 0
    # key_destinations = ""
    # key_departures = ""
    # payload_distance = 0
    # current_departure_city = 0
    # current_destination_city = 1

    route_len = 0
    len_of_list = len(list_route)
    i = 0

    while i < len_of_list:
        if i == len_of_list-1:
            break
        if list_route[0] == list_route[1]:
            route_len = 0
            return route_len
        else:
            route_len += int(dict_routes[list_route[i]][list_route[i+1]])
        i += 1

    # for key_departures, payload_destinations in sorted(dict_routes.items()):
    #     departure_city = list_route[current_departure_city]
    #     destination_city = list_route[current_destination_city]
    #     if departure_city in dict_routes:
    #         for key_destinations, payload_distance in \
    #                 sorted(payload_destinations.items()):
    #             route_distance += int(payload_distance)
    #     current_departure_city += 1
    #     current_destination_city += 1

    # for key_departures, payload_destinations in sorted(dict_routes.items()):
    #     for i in list_route:
    #         if key_departures in list_route:
    #             key_destinations = key_departures
    #
    #             for key_destinations, payload_distance in \
    #                     sorted(payload_destinations.items()):
    #                 if key_destinations in list_route:
    #                     # key_departures = key_destinations
    #
    #                     route_distance += int(payload_distance)
    #                     key_departures = key_destinations
                # key_departures = key_destinations
    #
    # for key_departures, payload_destinations in sorted(dict_routes.items()):
    #     for key_destinations, payload_distance in \
    #             sorted(payload_destinations.items()):
    #         print("yeet")
    #             # key_departures = key_destinations
    #
    #
    # for i in list_route:
    #
    #     if i in dict_routes:
    #         key_departures = i
    #         route_distance += int(payload_distance)


    return route_len

# Mieti kannattaako kutsua tästä vai mainista print_route_distance():a

def print_route_distance(dict_routes, lst_route, route_distance,
                         departure, destination):
    """
    fdssdfs
    :param dict_routes:
    :param lst_route:
    :param route_distance:
    :return:
    """

    len_of_list = len(lst_route)


    # try:
    for city in range(0, len_of_list-1, 1):
        print(f"{lst_route[city]}-", end="")

    print(f"{lst_route[-1]} ({route_distance} km)")

    # except ValueError:
    #     print(f"No route found between '{departure}' and "
    #           f"'{destination}'.")



# Helsinki-Lahti-Jyväskylä-Oulu-Rovaniemi (833 km)


def main():
    # distances.txt

    input_file = input("Enter input file name: ")

    # distance_data sanakirja sisältää kaikki haulutut tiedot kaikista
    # kaupungeista
    distance_data = read_distance_file(input_file)

    if distance_data is None:
        print(f"Error: '{input_file}' can not be read.")
        return

    while True:
        action = input("Enter action> ")

        if action == "":
            print("Done and done!")
            return

        # Switch toimii kuten if, muttei vaadi vertailulauseen x == y
        # toistamista jatkuvasti. Sen sijaan vaihtaa tapausta (engl. case)
        # annetun syötteen perusteella.

        elif "display".startswith(action):
            display_routes(distance_data)

        elif "add".startswith(action):
            ask_for_a_route(distance_data)

        elif "remove".startswith(action):
            remove_route(distance_data)

        elif "neighbours".startswith(action):
            city = input("Enter departure city: ")
            if city not in distance_data:
                print(f"Error: '{city}' is unknown.")
                continue
            # Toinen parametri city rajaa tulostuksen vain ko. kaupunkiin.
            display_routes(distance_data, city)

        elif "route".startswith(action):
            departure = input("Enter departure city: ")

            if departure not in distance_data:
                print(f"Error: '{departure}' is unknown.")
                continue

            destination = input("Enter destination city: ")
            
            if destination not in distance_data:
                print(f"No route found between '{departure}' and "
                      f"'{destination}'.")
                continue

            # elif destination not in distance_data[destination]:
            #     print(f"No route found between '{departure} and "
            #           f"'{destination}'.")
            #     continue

            route = find_route(distance_data, departure, destination)
            route_distance = calculate_route_distance(distance_data, route)
            print_route_distance(distance_data, route, route_distance, departure, destination)

        else:
            print(f"Error: unknown action '{action}'.")


if __name__ == "__main__":
    main()
