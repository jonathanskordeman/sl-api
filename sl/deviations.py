from sl.models import BaseModel
import sl.utils as utils


DEVIATIONS_API_URL = "http://api.sl.se/api2/deviations.json"


class Deviation(BaseModel):
    def __init__(self, **kwargs):
        self.default_params = {
            "Created": None,
            "MainNews": None,
            "SortOrder": None,
            "Header": None,
            "Details": None,
            "Scope": None,
            "DevCaseGid": None,
            "DevMessageVersionNumber": None,
            "ScopeElements": None,
            "FromDateTime": None,
            "UpToDateTime": None,
            "Updated": None
        }
        self._json_data = kwargs
        for (param, default) in self.default_params.items():
            setattr(self, utils.to_snake_case(param), kwargs.get(param, default))
