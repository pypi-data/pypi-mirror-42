"""
fritz.api_resources.model
~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: © 2019 by Fritz Labs Incorporated
:license: MIT, see LICENSE for more details.
"""

import fritz
from fritz.api_resources import fritz_object


class Model(fritz_object.FritzObject):
    """Fritz Model object."""

    OBJECT_NAME = "Model"

    @property
    def framework(self):
        """Gets associated framework for model.

        Returns: frameworks.ModelFramework
        """
        if self.model_format == "coreml":
            return fritz.frameworks.CORE_ML
        if self.model_format == "tflite":
            return fritz.frameworks.TENSORFLOW_LITE
        if self.model_format == "tfmobile":
            return fritz.frameworks.TENSORFLOW_MOBILE
        if self.model_format == "keras":
            return fritz.frameworks.KERAS

        return None
