import requests_mock
import os
import sl

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'data','real_time_departures.json')) as f:
    REAL_TIME_DEPARTURE_DATA=f.read()
with open(os.path.join(here, 'data','type_ahead.json')) as f:
    TYPE_AHEAD_DATA=f.read()
with open(os.path.join(here, 'data','deviations.json')) as f:
    DEVIATIONS_DATA = f.read()

@requests_mock.Mocker(kw='rmock')
class TestSlApiClient:
    def test_real_time_departure_deserialization(self, **kwargs):
        kwargs['rmock'].register_uri('GET', sl.REAL_TIME_DEPARTURES_API_URL, text=REAL_TIME_DEPARTURE_DATA)
        client = sl.ApiClient(real_time_departure_key='abc')
        res = client.get_real_time_departures(9001)

        assert isinstance(res, sl.Departure)

        assert len(res.buses) == 10
        for bus in res.buses:
            assert bus.to_json_string()
            assert isinstance(bus, sl.Bus)

        assert len(res.metros) == 12
        for metro in res.metros:
            assert isinstance(metro, sl.Metro)
            assert metro.to_json_string()
            if metro.deviations:
                assert isinstance(metro.deviations[0], sl.RealTimeDeviation)

        assert len(res.trains) == 10
        for train in res.trains:
            assert train.to_json_string()
            assert isinstance(train, sl.Train)
            if train.deviations:
                assert isinstance(train.deviations[0], sl.RealTimeDeviation)

        assert len(res.ships) == 2
        for ship in res.ships:
            assert ship.to_json_string()
            assert isinstance(ship, sl.Ship)
            if ship.deviations:
                assert isinstance(ship.deviations[0], sl.RealTimeDeviation)

        assert len(res.trams) == 5
        for tram in res.trams:
            assert tram.to_json_string()
            assert isinstance(tram, sl.Tram)
            if tram.deviations:
                assert isinstance(tram.deviations[0], sl.RealTimeDeviation)

        assert len(res.stop_point_deviations) == 1


    def test_type_ahead(self, **kwargs):
        kwargs['rmock'].register_uri('GET', sl.TYPE_AHEAD_API_URL, text=TYPE_AHEAD_DATA)
        client = sl.ApiClient(type_ahead_key='abc')
        res = client.get_type_ahead('abc')
        assert isinstance(res, list)
        assert len(res) == 10

        for site in res:
            assert isinstance(site, sl.Site)

    def test_deviations(self, **kwargs):
        kwargs['rmock'].register_uri('GET', sl.DEVIATIONS_API_URL, text=DEVIATIONS_DATA)
        client = sl.ApiClient(deviations_key='abc')
        res = client.get_deviations('abc')

        assert len(res) == 10

        for dev in res:
            assert isinstance(dev, sl.Deviation)