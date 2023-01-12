def read_file(input_filename):
    """Create a dictionary with individual contact information
       contained in nested dictionaries.
    :param input_filename: str, the name of the CSV-file
                           the information extracted from.
    :return: dict, the created dictionary with categorized contact information.
    """
    data_file = open(input_filename, mode="r")
    info = {}
    count = 0
#    parts = ""
    for line in data_file:
        line = line.rstrip()
        individual_info = {}
        if count == 0:
            indiv_info_keys = line.split(";")
        else:
            parts = line.split(";")
            for index in range(1, len(parts)):
                individual_info[indiv_info_keys[index]] = parts[index]
                info[parts[0]] = individual_info
        count += 1
    return info

def main():
    info = read_file("contacts.csv")
    # print(info["Mike"]["skype"])
if __name__ == "__main__":
    main()