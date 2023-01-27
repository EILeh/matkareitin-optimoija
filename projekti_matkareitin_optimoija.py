"""
COMP.CS.100 Ohjelmointi 1
3. projekti

Tekijä 1: Elli Lehtimäki
Opiskelijanumero: 151309919

Tekijä 2: Eetu Kuittinen
Opiskelijanumero: 150541820

Ohjelma tutkii kaupunkien välisiä etäisyyksiä ja niiden välisiä reittejä.
Ohjelman käyttöä varten tarvitaan CSV-muodossa formatoitu TXT-tiedosto.
Ohjelman alussa ohjelma yrittää avata tätä tiedostoa ohjelman ajokansiosta.
Mikäli avaaminen epäonnistuu, tulostuu poikkeuskäsittelyssä virheviesti ja
ohjelma suljetaan. Jos tiedoston avaaminen puolestaan onnistuu, sen sisältö
lisätään silmukassa rivi riviltä sanakirjaan.

Ohjelman tietorakenne on sisäkkäinen sanakirja, ts. sanakirja,
jonka hyötykuormana on toinen sanakirja. Arvot luetaan sanakirjaan niin, että
uloin avain on lähtökaupunki, sisemmän sanakirjan avain on kohdekaupunki ja
sisemmän sanakirjan hyötykuorma on näiden välinen etäisyys.

Ohjelmassa on lukuisia toimintoja. Se osaa mm. etsiä reittejä, lisätä uusia
reittejä, poistaa vanhoja reittejä kuin myös selvittää reittien olemassaoloa.
Suurimpaan osaan näistä operaatioista käytetään vain edellä mainittua
sanakirjaa, mutta välillä käytetään myös listaa, kuten halutun reitin
kaupunkien listaamiseen ja läpikäymiseen.
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

    :param data: dict, A data structure of an unspecified type (you decide)
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

    # MUUTTUJIEN ALUSTUKSET TIETOTYYPEITTÄIN AAKKOSJÄRJESTYKSESSÄ

    # Merkkijonot
    departure = ""
    destination = ""
    distance = ""

    # Sanakirjat
    dict_file_contents = {}

    try:
        # UTF-8 mahdollistaa "ääkkösten" käsittelyn
        text_file = open(file_name, mode="r", encoding="utf-8")

        # Lukee tiedoston sisällön riveittäin, kerää halutut tiedot talteen
        # omiin kenttiin ja laittaa arvoja sanakirjaan niin, että hakuavaimeksi
        # tulee rivin ensimmäinen kenttä eli haettava kaupunki.
        for line in text_file:
            line = line.strip()

            # Rivin kentät otetaan talteen omiin muuttujiinsa.
            departure, destination, distance = line.split(";")

            add_routes_to_dict(departure, destination, distance,
                               dict_file_contents)

        text_file.close()

    # Tiedoston luku epäonnistuu.
    except OSError:
        return None

    # Rivi ei noudata haluttua muotoilua (lähtökaupunki;kohdekaupunki;etäisyys).
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

    :param data: dict, A data structure containing the distance
           information between the known cities.
    :param city: str, the name of the city whose neighbours we
           are interested in.
    :return: list[str], the neighbouring city names in a list.
             Returns [], if <city> is unknown (i.e. not stored as
             a departure city in <data>) or if there are no
             arrows leaving from the <city>.
    """

    # MUUTTUJIEN ALUSTUKSET TIETOTYYPEITTÄIN AAKKOSJÄRJESTYKSESSÄ

    # Listat
    list_neighbouring_cities = []

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

    :param data: dict, A data structure containing the distance
           information between the known cities.
    :param departure: str, the name of the departure city.
    :param destination: str, the name of the destination city.
    :return: int | None, The distance between <departure> and
           <destination>. None if there is no direct connection
           between the two cities.
    """

    # MUUTTUJIEN ALUSTUKSET TIETOTYYPEITTÄIN AAKKOSJÄRJESTYKSESSÄ

    # Kokonaisluvut
    int_distance = 0

    # Haetaan etäisyys sanakirjasta, jossa se on sisin hyötykuorma, muunnetaan
    # se kokonaisluvuksi ja tallennetaan muuttujaan.
    int_distance = int(data[departure][destination])

    return int_distance


def command_display(dict_routes, city=""):
    """
    Etsii tiedot kaupunkien nimien merkkimääristä, jotta ne voidaan tulostaa
    halutussa muodossa funktiossa display_a_route.
    :param dict_routes: dict, sisältää tiedon kaupungeista ja niiden välisistä
           etäisyyksistä
    :param city: str, sisältää tiedon kaupungista
    :return: Python palauttaa implisiittisesti None-arvon
    """

    # MUUTTUJIEN ALUSTUKSET TIETOTYYPEITTÄIN AAKKOSJÄRJESTYKSESSÄ

    # Kokonaisluvut
    leftover_space_of_departures = 0
    leftover_space_of_destinations = 0
    leftover_space_of_distance = 0
    len_original_space_of_str_departures = 14
    len_original_space_of_str_destinations = 14
    len_original_space_of_str_distance = 5

    # Merkkijonot
    str_payload_distance = ""

    # Hankitaan sisäkkäisillä silmukoilla tiedot kaupungeista ja haetaan
    # tieto jokaisen kaupungin kohdalla siitä, kuinka monta välilyöntiä
    # tulostukseen haltutaan.
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
                display_a_route(len_str_departures_with_spaces,
                                len_str_destinations_with_spaces,
                                len_str_distance_with_spaces)

            # Jos lähtökaupunki syötetään, tallennetaan lähtökaupungin tiedot
            # omaan muuttujaan ja tulostetaan lähtökaupunki ja sen
            # naapurikaupungit print_routes funktiossa.
            elif key_departures == city:
                len_str_city_with_spaces = city + " " * \
                                           leftover_space_of_departures

                display_a_route(len_str_city_with_spaces,
                                len_str_destinations_with_spaces,
                                len_str_distance_with_spaces)


def display_a_route(str_departure, str_destination, str_distance):
    """
    Tulostaa kaupungit halutussa muodossa.
    :param str_departure: str, lähtökaupungin nimen merkkien määrä
           kaupunkikohtaisesti ja välilyönnit merkkien määrästä riippuen
    :param str_destination: str, kohdekaupungin nimen merkkien määrä
           kaupunkikohtaisesti ja välilyönnit merkkien määrästä riippuen
    :param str_distance: str, etäisyyden merkkien määrä ja välilyönnit merkkien
           määrästä riippuen
    :return: Python palauttaa implisiittisesti None-arvon.
    """

    print(str_departure + str_destination + str_distance)


def add_routes_to_dict(departure, destination, distance, dict_routes):
    """
    Tarkistaa löytyykö lähtökaupunki sanakirjasta, ja lisää syötetyn
    lähtökaupungin, kohdekaupungin ja niiden välisen etäisyyden sanakirjaan.
    Jos lähtökaupunki löytyy jo sanakirjasta, lisätään uusi reitti syötettyyn
    kohdekaupunkiin.
    :param departure: str, käyttäjän syöttämä lähtökaupunki
    :param destination: str, käyttäjän syöttämä kohdekaupunki
    :param distance: int, käyttäjän syöttämä etäisyys
    :param dict_routes: dict, sisältää tiedon kaupungeista
    :return: Python palauttaa implisiittisesti None-arvon
    """

    # Jos rivillä olevaa kaupunkia ei löydy sanakirjasta, luodaan
    # sanakirjaan kokonaan uusi avain lähtökaupungin nimellä.
    if not city_in_dict_routes(departure, dict_routes):
        dict_routes[departure] = {destination: distance}

    # Jos lähtökaupunki löytyy jo sanakirjasta, päivitetään vain sieltä
    # lähteviä reittejä.
    else:
        dict_routes[departure][destination] = distance


def command_add(dict_routes):
    """
    Kysyy käyttäjältä kaupungit ja niiden välisen etäisyyden.
    :param dict_routes: dict, sisältää reitit
    :return: Python palauttaa implisiittisesti None-arvon
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

    # Tarkistaa löytyykö kohdekaupunki sanakirjasta
    if not city_in_dict_routes(destination_city, dict_routes):

        # Kohdekaupunki lisätään sanakirjaan tyhjällä hyötykuormalla. Tämä teh-
        # dään siksi, että if in toimisi muualla ohjelmassa oikein, sillä in
        # katsoo vain avaimia, mutta kaupunki voi olla myös pelkkä hyötykuorma.
        dict_routes[destination_city] = {}

    # Etäisyys otetaan aluksi vastaan merkkijonona, jotta voidaaan tarkistaa,
    # sisältääkö syöte kelvottomia arvoja eli tässä tapauksessa muita kuin
    # numeroita.
    str_distance_between_cities = input("Distance: ")

    # Etäisyys yritetään muuttaa kokonaisluvuksi.
    try:
        distance_between_cities = int(str_distance_between_cities)

    # Jos kokonaisluvuksi muuttaminen ei onnistu, tulostuu virheilmoitus.
    except ValueError:
        print(f"Error: '{str_distance_between_cities}' is not an integer.")
        return None

    # Jos etäisyys oli kokoniasluku, kutsutaan funktiota reitin lisäämiseksi
    # sanakirjaan.
    add_routes_to_dict(departure_city, destination_city,
                       distance_between_cities, dict_routes)


def command_remove(dict_routes):
    """
    Kysyy reitin, joka halutaan poistaa. Jos lähtökaupunki on tuntematon tai
    reittiä ei löydy, tulostetaan virheilmoitus.
    :param dict_routes: dict, sisältää tiedon kaupungeista
    :return: Palataan pois funktiosta (= palautuu None-arvo).
    """
    # MUUTTUJIEN ALUSTUKSET TIETOTYYPEITTÄIN AAKKOSJÄRJESTYKSESSÄ

    # Merkkijonot
    departure_city = ""
    destination_city = ""

    # Käytetään string.title() metodia aakkosjärjestyksen varmistamiseksi.
    # Ilman tätä järjestäisi isot ja pienet kirjaimet "omiksi listoikseen"
    # sorted:illa, ts. menetettäisiin oikea aakkosjärjestys.
    departure_city = input("Enter departure city: ").title()

    # Jos lähtökaupunkia ei löydy sanakirjasta, ei kysytä kohdekaupunkia vaan
    # tulostetaan suoraan error.
    if not city_in_dict_routes(departure_city, dict_routes):
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
    Laskee kaupunkien välisen etäisyyden ja palauttaa tiedon reitin pituudesta.
    :param dict_routes: dict, sisältää tiedon kaikista kaupungeista
    :param list_route: list, sisältää tiedon reitin kaupungeista
    :return: int, palauttaa reitin pituuden
    """

    # MUUTTUJIEN ALUSTUKSET TIETOTYYPEITTÄIN AAKKOSJÄRJESTYKSESSÄ

    # Kokonaisluvut
    city_at_index = 0
    list_length = len(list_route)
    route_length = 0

    # Ottaa lähtökaupungiksi kaupungin kyseisellä indeksillä sekä
    # kohdekaupungiksi kaupungin, joka on seuraavassa indeksissä. Korottaa
    # indeksiä yhdellä joka kierroksella, jolloin aiempi kohdekaupunki on uusi
    # lähtökaupunki, kunnes indeksi on yhden pienempi kuin listan pituus on, eli
    # viimeinen indeksi (pituus on yhden suurempi).
    # Palauttaa reitin pituuden.
    while city_at_index < list_length-1:

        # Jos lähtökaupunki on sama kuin kohdekaupunki, palautetaan reitin
        # pituus nollana.
        if list_route[0] == list_route[1]:
            route_length = 0
            return route_length
        else:
            route_length += int(dict_routes[list_route[city_at_index]]
                                [list_route[city_at_index + 1]])

        city_at_index += 1

    return route_length


def print_route_distance(list_route, route_distance, destination):
    """
    Tulostaa syötetyt lähtö- ja kohdekaupungit halutussa muodossa sekä niiden
    välisen etäisyyden.
    :param list_route: list, reittiin kuuluvat kaupungit
    :param route_distance: int, reitin pituus
    :param departure: str, kohdekaupunki, jota käytetään tulostukseen
    :return: Python palauttaa implisiittisesti None-arvon
    """

    # MUUTTUJIEN ALUSTUKSET TIETOTYYPEITTÄIN AAKKOSJÄRJESTYKSESSÄ

    # Kokonaisluvut
    list_length = len(list_route)

    # Listalta tulostetaan halutussa muodossa kaikki sieltä löytyvät kaupungit
    # kohdekaupunkia lukuun ottamatta.
    for city in range(0, list_length - 1, 1):
        print(f"{list_route[city]}-", end="")

    # Viimeinen kaupunki tulostetaan erikseen, jotta sen perään ei tulisi
    # kaupunkien väliin tulevaa väliviivaa.
    print(f"{destination} ({route_distance} km)")


def command_neighbours(distance_data):
    """
    Kysyy käyttäjältä lähtökaupunkia ja etsii sen kaikki naapurikaupungit. Jos
    lähtökaupunkia ei löydy, tulostetaan virheilmoitus.
    :param distance_data: dict, sisältää tiedon kaikista kaupungeista

    """

    # MUUTTUJIEN ALUSTUKSET TIETOTYYPEITTÄIN AAKKOJÄRJESTYKSESSÄ

    # Merkkijonot
    city = ""

    city = input("Enter departure city: ").title()

    # Jos lähtökaupunkia ei löydy sanakirjasta, tulostetaan error.
    if not city_in_dict_routes(city, distance_data):
        print(f"Error: '{city}' is unknown.")

    # Jos lähtökaupunki löytyy, toinen parametri city rajaa tulostuksen vain
    # kyseessä olevaan kaupunkiin.
    command_display(distance_data, city)


def city_in_dict_routes(city, dict_routes):
    """
    Tarkistaa löytyykö haluttua kaupunkia kaupunkisanakirjasta.
    :param city: str, etsittävä kaupunki
    :param dict_routes: dict, kaupunkisanakirja.
    :return: palauttaa totuusarvon tehdyn löydön perusteella.
    """

    if city not in dict_routes:
        return False

    return True


def command_route(distance_data):
    """
    Etsii reitin syötettävien kaupunkien välisen reitin.
    :param distance_data: dict, sisältää tiedon kaikista kaupungeista
    :return: Palataan pois funktiosta (= palautuu None-arvo).
    """

    # MUUTTUJIEN ALUSTUKSET TIETOTYYPEITTÄIN AAKKOJÄRJESTYKSESSÄ

    # Kokonaisluvut
    route_distance = 0

    # Listat
    route = []

    # Merkkijonot
    departure = ""
    destination = ""

    departure = input("Enter departure city: ").title()

    # Jos lähtökaupunkia ei löydy sanakirjasta, tulostetaan error.
    if not city_in_dict_routes(departure, distance_data):
        print(f"Error: '{departure}' is unknown.")
        return

    destination = input("Enter destination city: ").title()

    # Tarkistaa omassa funktiossaan löytyykö kaupunkien väliltä yhteyksiä.
    route = find_route(distance_data, departure, destination)

    # Jos yhteyttä kaupunkien välille ei ole, tulostetaan error.
    if not route:
        print(f"No route found between '{departure}' and '"
              f"{destination}'.")
        return

    # Reitin löytyessä laskee sen pituuden siihen tarkoitetussa funktiossa.
    route_distance = calculate_route_distance(distance_data, route)

    # Tulostaa kaupungit ja niiden välisen reitin halutussa muodossa.
    print_route_distance(route, route_distance, destination)


def main():
    # distances.txt

    input_file = input("Enter input file name: ")

    # distance_data sanakirja sisältää kaikki haulutut tiedot kaikista
    # kaupungeista.
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
            command_display(distance_data)

        elif "add".startswith(action):
            command_add(distance_data)

        elif "remove".startswith(action):
            command_remove(distance_data)

        elif "neighbours".startswith(action):
            command_neighbours(distance_data)

        elif "route".startswith(action):
            command_route(distance_data)

        else:
            print(f"Error: unknown action '{action}'.")


if __name__ == "__main__":
    main()
