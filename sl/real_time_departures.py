import sl.utils as utils
from sl.models import BaseModel

REAL_TIME_DEPARTURES_API_URL = 'http://api.sl.se/api2/realtimedeparturesV4.json'


class Departure(BaseModel):
    def __init__(self, **kwargs):
        self.default_params = {
            'LatestUpdate': None,
            'DataAge': None,
            'Buses': None,
            'Metro': None,
            'Trains': None,
            'Trams': None,
            'Ships': None,
            'StopPointDeviations': None
        }
        for (param, default) in self.default_params.items():
            setattr(self, utils.to_snake_case(param), kwargs.get(param, default))
        if 'Buses' in kwargs:
            self.buses = [Bus.NewFromJson(b) for b in kwargs['Buses']]
        if 'Metros' in kwargs:
            self.metros = [Metro.NewFromJson(m) for m in kwargs['Metros']]
        if 'Trains' in kwargs:
            self.trains = [Train.NewFromJson(t) for t in kwargs['Trains']]
        if 'Trams' in kwargs:
            self.trams = [Tram.NewFromJson(t) for t in kwargs['Trams']]
        if 'Ships' in kwargs:
            self.ships = [Ship.NewFromJson(s) for s in kwargs['Ships']]
        if 'StopPointDeviations' in kwargs:
            self.stop_point_deviations = [StopPointDeviation.NewFromJson(s) for s in kwargs['StopPointDeviations']]


class Vehicle(BaseModel):
    def __init__(self, **kwargs):
        self.default_params = {
            'SiteId': None,
            'TransportMode': None,
            'StopAreaName': None,
            'StopAreaNumber': None,
            'StopPointNumber': None,
            'LineNumber': None,
            'Destination': None,
            'TimeTabledDateTime': None,
            'ExpectedDateTime': None,
            'DisplayTime': None,
            'Deviations': None,
            'JourneyDirection': None
        }


    def _apply_params(self, data, **kwargs):
        for (param, default) in self.default_params.items():
            setattr(self, utils.to_snake_case(param), data.get(param, default))

        if 'Deviations' in data and data['Deviations']:
            self.deviations = [RealTimeDeviation.NewFromJson(dev) for dev in data['Deviations']]


class Bus(Vehicle):
    def __init__(self, **kwargs):
        super().__init__()
        self.default_params['GroupOfLine'] = None
        self.default_params['StopPointDesignation'] = None

        self._apply_params(kwargs)
        # for (param, default) in self.default_params.items():
        #     setattr(self, utils.to_snake_case(param), kwargs.get(param, default))


class Train(Vehicle):
    def __init__(self, **kwargs):
        super().__init__()
        self.default_params['SecondaryDestinationName'] = None
        self.default_params['StopPointDesignation'] = None
        self._apply_params(kwargs)
        # for (param, default) in self.default_params.items():
        #     setattr(self, utils.to_snake_case(param), kwargs.get(param, default))


class Tram(Vehicle):
    def __init__(self, **kwargs):
        super().__init__()
        self.default_params['GroupOfLine'] = None
        self.default_params['StopPointDesignation'] = None
        self._apply_params(kwargs)
        # for (param, default) in self.default_params.items():
        #     setattr(self, utils.to_snake_case(param), kwargs.get(param, default))


class Ship(Vehicle):
    def __init__(self, **kwargs):
        super().__init__()
        self.default_params['GroupOfLine'] = None
        self._apply_params(kwargs)
        # for (param, default) in self.default_params.items():
        #     setattr(self, utils.to_snake_case(param), kwargs.get(param, default))


class Metro(Vehicle):
    def __init__(self, **kwargs):
        super().__init__()
        self.default_params['DepartureGroupId'] = None
        self.default_params['GroupOfLine'] = None
        self.default_params['GroupOfLineId'] = None
        self.default_params['PlatformMessage'] = None
        self._apply_params(kwargs)
        # for (param, default) in self.default_params.items():
        #     setattr(self, utils.to_snake_case(param), kwargs.get(param, default))


class RealTimeDeviation(BaseModel):
    def __init__(self, **kwargs):
        self.default_params = {
            'Consequence': None,
            'ImportanceLevel': None,
            'Text': None
        }
        for (param, default) in self.default_params.items():
            setattr(self, utils.to_snake_case(param), kwargs.get(param, default))


class StopInfo(BaseModel):
    def __init__(self, **kwargs):
        self.default_params = {
            'GroupOfLine': None,
            'StopAreaName': None,
            'StopAreaNumber': None,
            'TransportMode': None
        }
        for (param, default) in self.default_params.items():
            setattr(self, utils.to_snake_case(param), kwargs.get(param, default))


class StopPointDeviation(BaseModel):
    def __init__(self, **kwargs):
        self.default_params = {
            'StopInfo': None,
            'Deviation': None
        }
        for (param, default) in self.default_params.items():
            setattr(self, utils.to_snake_case(param), kwargs.get(param, default))
        if 'StopInfo' in kwargs:
            self.stop_info = StopInfo.NewFromJson(kwargs.get('StopInfo'))
        if 'Deviation' in kwargs:
            self.deviation = RealTimeDeviation.NewFromJson(kwargs.get('Deviation'))
