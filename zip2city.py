import sys, os, csv, urllib, json

def get_file_names():
    """
    Get system arguments for input
    and out put files.
    """
    input_file = sys.argv[1]
    filename, extension = os.path.splitext(input_file)
    if extension != '.csv':
        sys.exit('Error, incorrect input file provided.')
    if len(sys.argv) > 2:
        output_file = sys.argv[2]+extension
    else:
        output_file = filename+'_output'+extension
    return input_file, output_file

def get_zips(input_file):
    """
    Get values for each filled row
    in the first column of a given
    csv file.
    """
    zips = []
    with open(input_file, 'rU') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            zips.append(row[0])
    return zips

def get_cities(zipcodes):
    """
    Uses zipcodes to lookup
    corresponding cities.
    Uses maps.googleapis.com
    """
    zip_cities = dict()
    for idx, zipcode in enumerate(zipcodes):
        url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+zipcode+'&sensor=true'
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        city = data['results'][0]['address_components'][1]['long_name']
        state = data['results'][0]['address_components'][3]['long_name']
        zip_cities.update({idx: [zipcode, city, state]})
    return zip_cities



def make_output_csv(zips_cities, output_file):
    """
    Takes dictionary of zips with
    corresponding data.
    Makes output csv file
    """
    if sys.version_info.major == 3:
        writer = csv.writer(open(output_file, 'w', newline=''))
    else:
        writer = csv.writer(open(output_file, 'wb'))
    for key, location in zips_cities.items():
        writer.writerow([location[0], location[1], location[2]])
    return output_file

def main():
    input_file, output_file = get_file_names()
    zipcodes = get_zips(input_file)
    if sys.version_info.major == 3:
        from async import get_cities_async
        zips_cities = get_cities_async(zipcodes)
    else:
        zips_cities = get_cities(zipcodes)
    new_file = make_output_csv(zips_cities, output_file)
    print("Done. Created: {}".format(new_file))

if __name__ == '__main__':
    if 'help' == sys.argv[1]:
        f = open('readme.txt', 'r')
        print(f.read())
        f.close()
    else:
        main()
