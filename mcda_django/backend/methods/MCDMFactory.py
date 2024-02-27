from .MCDMTopsis import MCDMTOPSIS
from .MCDMCopras import MCDMCOPRAS
from .MCDMSpotis import MCDMSPOTIS


class MCDAMethodFactory:
    _available_methods = {
        "topsis": MCDMTOPSIS,
        "copras": MCDMCOPRAS,
        "spotis": MCDMSPOTIS,
    }

    @staticmethod
    def __call__(method_name, *args, **kwargs):
        if method_name in MCDAMethodFactory._available_methods:
            return MCDAMethodFactory._available_methods[method_name](*args, **kwargs)
        else:
            raise ValueError(f"Unknown method, name: {method_name}")

    @staticmethod
    def get_available_methods():
        return MCDAMethodFactory._available_methods.keys()
        