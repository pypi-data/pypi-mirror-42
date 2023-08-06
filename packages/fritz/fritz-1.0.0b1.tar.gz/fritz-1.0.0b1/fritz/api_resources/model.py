"""
fritz.api_resources.model
~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: © 2019 by Fritz Labs Incorporated
:license: MIT, see LICENSE for more details.
"""


from fritz import frameworks
from fritz.api_resources import fritz_object


class Model(fritz_object.FritzObject):
    """Fritz Model object."""
    OBJECT_NAME = 'Model'

    @property
    def framework(self):
        """Gets associated framework for model.

        Returns: `frameworks.ModelFramework`
        """
        if self.model_format == 'coreml':
            return frameworks.Frameworks.CORE_ML
        if self.model_format == 'tflite':
            return frameworks.Frameworks.TENSORFLOW_LITE
        if self.model_format == 'tfmobile':
            return frameworks.Frameworks.TENSORFLOW_MOBILE
        if self.model_format == 'keras':
            return frameworks.Frameworks.KERAS

        return None
