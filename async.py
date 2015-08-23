def get_cities_async(zipcodes):
    """
    Uses Python 3's async library.
    Uses zipcodes to lookup
    corresponding cities.
    Uses maps.googleapis.com
    """
    import asyncio, json
    try:
        import aiohttp
    except:
        sys.exit('You need aiohttp.')

    zip_cities = dict()

    @asyncio.coroutine
    def async_call(zipcode,idx):
        url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+zipcode+'&sensor=true'
        response = yield from aiohttp.request('get', url)
        string = (yield from response.read()).decode('utf-8')
        data = json.loads(string)
        city = data['results'][0]['address_components'][1]['long_name']
        state = data['results'][0]['address_components'][3]['long_name']
        zip_cities.update({idx: [zipcode, city, state]})

    loop = asyncio.get_event_loop()
    tasks = [asyncio.async(async_call(z, i)) for i, z in enumerate(zipcodes)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    return zip_cities