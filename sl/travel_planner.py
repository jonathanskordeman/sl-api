from sl.models import BaseModel
import sl.utils as utils

TRAVEL_PLANNER_API_URL = 'http://api.sl.se/api2/TravelplannerV2/trip.json'


class Trip(BaseModel):
    def __init__(self, **kwargs):
        self.default_params = {
            'dur': None,
            'chg': None,
            'co2': None,
            'valid': None,
            'alternative': None,
            'PriceInfo': None,
            'LegList': None,
            'RTUMessages': None,
            'Notes': None
        }
        for (param, default) in self.default_params.items():
            setattr(self, utils.to_snake_case(param), kwargs.get(param, default))
        if 'PriceInfo' in kwargs:
            self.price_info = {}
            if 'TariffZones' in kwargs.get('PriceInfo').keys():
                self.price_info['tariff_zones'] = kwargs.get('PriceInfo')['TariffZones']['$']
            if 'TariffRemark' in kwargs.get('PriceInfo').keys():
                self.price_info['tariff_remark'] = kwargs.get('PriceInfo')['TariffRemark']['$']
        if 'LegList' in kwargs:
            self.leg_list = LegList.NewFromJson(kwargs.get('LegList'))
        if 'RTUMessages' in kwargs:
            rtu_messages = []
            for message in kwargs.get('RTUMessages'):
                rtu_messages.append({'rtu_message': message})
            self.rtu_messages = rtu_messages
        if 'Notes' in kwargs:
            notes = []
            for note in kwargs.get('Notes'):
                notes.append({'note': note})
            self.notes = notes


class LegList(BaseModel):
    def __init__(self, **kwargs):
        self.default_params = {'Leg': None}
        for (param, default) in self.default_params.items():
            setattr(self, utils.to_snake_case(param), kwargs.get(param, default))
        if 'Leg' in kwargs:
            self.leg = [Leg.NewFromJson(leg) for leg in kwargs['Leg']]


class Leg(BaseModel):
    def __init__(self, **kwargs):
        self.default_params = {
            'idx': None,
            'name': None,
            'type': None,
            'dir': None,
            'line': None,
            'hide': None,
            'dist': None,
            'Origin': None,
            'Destination': None,
            'JourneyDetailRef': None,
            'GeometryRef': None
        }
        for (param, default) in self.default_params.items():
            setattr(self, utils.to_snake_case(param), kwargs.get(param, default))
        if 'Origin' in kwargs:
            self.origin = LegPoint.NewFromJson(kwargs.get('Origin'))
        if 'Destination' in kwargs:
            self.destination = LegPoint.NewFromJson(kwargs.get('Destination'))
        if 'JourneyDetailRef' in kwargs:
            self.journey_detail_ref = LegRef.NewFromJson(kwargs.get('JourneyDetailRef'))
        if 'GeometryRef' in kwargs:
            self.geometry_ref = LegRef.NewFromJson(kwargs.get('GeometryRef'))


class LegPoint(BaseModel):
    def __init__(self, **kwargs):
        self.default_params = {
            'name': None,
            'type': None,
            'id': None,
            'routeIdx': None,
            'lon': None,
            'lat': None,
            'time': None,
            'date': None,
            'track': None
        }
        for (param, default) in self.default_params.items():
            setattr(self, utils.to_snake_case(param), kwargs.get(param, default))


class LegRef(BaseModel):
    def __init__(self, **kwargs):
        self.default_params = {
            'ref': None
        }
        for (param, default) in self.default_params.items():
            setattr(self, utils.to_snake_case(param), kwargs.get(param, default))
