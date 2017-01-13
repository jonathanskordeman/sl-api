import requests
import sl




def query_real_time_departures(api_key, site_id, time_window=60, transport_selection_override=None, **kwargs):
    if not transport_selection_override:
        transport_selection_override = {'bus': True, 'metro': True, 'train': True, 'tram': True, 'Ship': True}
    params = {'key': api_key, 'siteid': site_id, 'timewindow': time_window}
    params.update(transport_selection_override)
    if kwargs:
        params.update(kwargs)
    response = requests.get(sl.REAL_TIME_DEPARTURES_API_URL, params)
    response_data = response.json()
    departure = None
    if response_data['ResponseData']:
        departure = sl.Departure.NewFromJson(response_data['ResponseData'])
    return departure


def query_deviations(api_key, search_string=None, stations_only=True, max_results=10):
    params = {'key': api_key, 'searchstring': search_string, 'stationsonly': stations_only, 'maxresults': max_results}
    response = requests.get(sl.DEVIATIONS_API_URL, params)
    response_payload = response.json()
    if response_payload['ResponseData']:
        deviations = [sl.Deviation.NewFromJson(deviation) for deviation in
                      response_payload['ResponseData']]
        return deviations


def query_type_ahead(api_key, search_string, stations_only=True, max_results=10):
    params = {'key': api_key, 'searchstring': search_string, 'stationsonly': stations_only, 'maxresults': max_results}
    response = requests.get(sl.TYPE_AHEAD_API_URL, params)
    response_payload = response.json()
    if response_payload['ResponseData']:
        places = [sl.Site.NewFromJson(site) for site in response_payload['ResponseData']]
        return places
    return


def query_travel_planner(api_key, origin, dest, date=None, time=None, **kwargs):
    params = {'key': api_key, 'date': date, 'time': time}
    if isinstance(origin, dict):
        params.update(origin)
    else:
        params['originId'] = origin
    if isinstance(dest, dict):
        params.update(dest)
    else:
        params['destId'] = dest
    if kwargs:
        params.update(kwargs)

    response = requests.get(sl.TRAVEL_PLANNER_API_URL, params)
    response_data = response.json()
    if response_data['TripList']:
        trips = [sl.Trip.NewFromJson(trip) for trip in response_data['TripList']['Trip']]
        return trips
    return


class ApiClient(object):
    def __init__(self, api_keys=None, type_ahead_key=None, real_time_departure_key=None, travel_planner_key=None,
                 deviations_key=None):
        """
        Convenience client for accessing the SL API.
        :param api_keys: Dict containing the api_keys
        :param type_ahead_key:
        :param real_time_departure_key:
        :param travel_planner_key:
        :param deviations_key:
        :return:
        """
        self._api_keys = {'type_ahead_key': type_ahead_key, 'real_time_departure_key': real_time_departure_key,
                          'travel_planner_key': travel_planner_key, 'deviations_key': deviations_key}
        if api_keys:
            for (key, value) in api_keys.items():
                self._api_keys[key] = value

    def get_type_ahead(self, search_string, stations_only=True, max_results=10):
        if not (self._api_keys['type_ahead_key']):
            raise Exception('Api key not found')
        return query_type_ahead(self._api_keys['type_ahead_key'], search_string, stations_only, max_results)

    def get_real_time_departures(self, site_id, time_window=60, transport_selection_override=None):
        if not (self._api_keys['real_time_departure_key']):
            raise Exception('API key for real_time_departure not supplied')
        return query_real_time_departures(self._api_keys['real_time_departure_key'], site_id,
                                          time_window, transport_selection_override)

    def get_travel_plan(self, origin, dest, date=None, time=None, **kwargs):
        if not (self._api_keys['travel_planner_key']):
            raise Exception('API key for travel_planner not supplied')
        return query_travel_planner(self._api_keys['travel_planner_key'], origin, dest, date, time, **kwargs)

    def get_deviations(self, search_string=None, stations_only=True, max_results=10):
        if not (self._api_keys['deviations_key']):
            raise Exception('API key for deviations not supplied')
        return query_deviations(self._api_keys['deviations_key'], search_string, stations_only, max_results)