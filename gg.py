[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 77825, 77826, 77825, 79238, 77825, 74846, 5548, 2112, 5548, 45588],
 [0, 85342, 0, 5147, 0, 2770, 0, 8420, 79286, 87371, 79286, 102144],
 [0, 82238, 4300, 0, 4300, 3791, 4300, 7753, 81180, 84267, 81180, 101818],
 [0, 85342, 0, 5147, 0, 2770, 0, 8420, 79286, 87371, 79286, 102144],
 [0, 85128, 3702, 6139, 3702, 0, 3702, 12171, 84069, 87157, 84069, 103947],
 [0, 85342, 0, 5147, 0, 2770, 0, 8420, 79286, 87371, 79286, 102144],
 [0, 82508, 7453, 7172, 7453, 10358, 7453, 0, 76139, 84537, 76139, 101220],
 [0, 3783, 77535, 77536, 77535, 78948, 77535, 74556, 0, 3560, 0, 40769],
 [0, 2959, 79693, 79694, 79693, 81107, 79693, 76715, 3303, 0, 3303, 42743],
 [0, 3783, 77535, 77536, 77535, 78948, 77535, 74556, 0, 3560, 0, 40769],
 [0, 37626, 89250, 89251, 89250, 90663, 89250, 86271, 35225, 36644, 35225, 0]]


def create_distance_matrix(deliverers_location, orders):
    data = create_data(deliverers_location, orders)
    addresses = data["addresses"]
    API_key = data["API_key"]
    # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
    max_elements = 100
    num_addresses = len(addresses)
    # Maximum number of rows that can be computed per request.
    max_rows = max_elements // num_addresses
    # num_addresses = q * max_rows + r (q = 2 and r = 4 in this example).
    q, r = divmod(num_addresses, max_rows)
    dest_addresses = addresses
    distance_matrix = []
    # add the zeros row at the beginning of the matrix >> end node distance
    end_node = []
    for i in range(len(addresses) + 1):
        end_node.append(0)
    distance_matrix.append(end_node)
    # Send q requests, returning max_rows rows per request.
    for i in range(q):
        origin_addresses = addresses[i * max_rows: (i + 1) * max_rows]
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)

    # Get the remaining remaining r rows, if necessary.
    if r > 0:
        origin_addresses = addresses[q * max_rows: q * max_rows + r]
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)

    # Add a row of zeros and a zero at the start of each row
    dist_matrix = []
    for row in distance_matrix:
        if len(row) == len(
                addresses) + 1:  # check if the zero is already added to the beginning of the row
            dist_matrix.append(row)  # just add row to the new list
        elif len(row) == len(addresses):
            row.insert(0, 0)  # insert zero at the beginning and append row
            dist_matrix.append(row)
    distance_matrix = dist_matrix
    return distance_matrix


