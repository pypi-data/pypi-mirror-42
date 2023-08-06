"""
fritz.fritz_object
~~~~~~~~~~~~~~~~~~~

:copyright: © 2019 by Fritz Labs Incorporated
:license: MIT, see LICENSE for more details.
"""
import json


class FritzObject(object):
    """An object from the API.

    Subclassed objects are used to define interactions with the API.
    """
    def __init__(self, **kwargs):
        self._data = kwargs

    def __repr__(self):
        identity_parts = [type(self).__name__]

        if isinstance(self.uid, str):
            identity_parts.append("uid=%s" % (self.uid))

        unicode_repr = "<%s> JSON: %s" % (
            " ".join(identity_parts),
            str(self),
        )

        return unicode_repr

    def __str__(self):
        return json.dumps(
            self._data,
            sort_keys=True,
            indent=2,
        )

    def __getattr__(self, key):
        if key[0] == "_":
            raise AttributeError(key)

        try:
            return self._data[key]
        except KeyError as err:
            raise AttributeError(*err.args)
