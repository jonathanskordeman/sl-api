from sl.models import BaseModel
import sl.utils as utils


TYPE_AHEAD_API_URL = 'http://api.sl.se/api2/typeahead.json'


class Site(BaseModel):
    def __init__(self, **kwargs):
        self.default_params = {
            'Name': None,
            'SiteId': None,
            'Type': None,
            'X': None,
            'Y': None
        }
        self._json_data = kwargs
        for (param, default) in self.default_params.items():
            setattr(self, utils.to_snake_case(param), kwargs.get(param, default))
