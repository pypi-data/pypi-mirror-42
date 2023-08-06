"""
fritz.frameworks
~~~~~~~~~~~~~~~~

:copyright: © 2019 by Fritz Labs Incorporated
:license: MIT, see LICENSE for more details.
"""
import io
import os
import tempfile


class ModelFramework(object):
    """Defines a specific model framework"""

    def __init__(self, name, extension, file_cls):
        self.name = name
        self.extension = extension
        self._file_cls = file_cls

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"ModelFramework(name={self.name} extension={self.extension})"

    def as_framework_filename(self, filename):
        """Generate filename that representing a model of this framework.

        Args:
            filename (str): filename (i.e. 'mobilenet_v2.h5')

        Returns: str
        """
        file_base = os.path.splitext(os.path.basename(filename))[0]
        return file_base + self.extension

    def to_file(self, model):
        """Build FrameworkFileBase object for Framework.

        Args:
            model: Model

        Returns: FrameworkFileBase
        """
        return self._file_cls(model)

    def build_file(self, path):
        """Build FrameworkFileBase object for a given path.

        Args:
            path: String

        Returns: FrameworkFileBase
        """
        return self._file_cls.build_from_file(path)


class FrameworkFileBase(object):
    """Base class to wrap models for interacting with Fritz."""

    def __init__(self, framework, model):
        self.framework = framework
        self.model = model

    def to_bytes(self):
        """Convert model to bytes.

        Returns: io.BytesIO object
        """
        raise NotImplementedError("Subclass class must implement")

    @classmethod
    def build_from_file(cls, path):
        """Build Framework File from model path.

        Args:
            path (str): Path to file.

        Returns: FrameworkFileBase instance.
        """
        raise NotImplementedError("Subclass class must implement")


class KerasFile(FrameworkFileBase):
    """Wrapper class for Keras model."""

    def __init__(self, model):
        super().__init__(KERAS, model)

    def to_bytes(self):
        # need to actually get the bytes here.
        tmp_file = tempfile.NamedTemporaryFile()
        self.model.save(tmp_file.name)
        tmp_file.seek(0)

        return tmp_file.read()

    @classmethod
    def build_from_file(cls, path):
        """Build KerasFile from model path.

        Args:
            path (str): Path to keras file.

        Returns: KerasFile instance.
        """
        # Keras is imported here so that we don't load keras and tensorflow
        # right away on all fritz imports.
        import keras

        model = keras.models.load_model(path)
        return cls(model)


# Have not implemented build_from_file
# pylint: disable=abstract-method
class CoreMLFile(FrameworkFileBase):
    """Wrapper class for Core ML model."""

    def __init__(self, model):
        super().__init__(CORE_ML, model)

    def to_bytes(self):
        serialized_spec = self.model.get_spec().SerializeToString()
        return io.BytesIO(serialized_spec)


# Have not implemented build_from_file
# pylint: disable=abstract-method
class TensorFlowLiteFile(FrameworkFileBase):
    """Wrapper class for TensorFlow Lite model."""

    def __init__(self, model):
        super().__init__(TENSORFLOW_LITE, model)

    def to_bytes(self):
        return io.BytesIO(self.model)


# Have not implemented build_from_file
# pylint: disable=abstract-method
class TensorFlowMobileFile(FrameworkFileBase):
    """Wrapper class for TensorFlow Mobile model."""

    def __init__(self, model):
        super().__init__(TENSORFLOW_MOBILE, model)

    def to_bytes(self):
        return io.BytesIO(self.model)


TENSORFLOW_LITE = ModelFramework("tflite", ".tflite", TensorFlowLiteFile)
TENSORFLOW_MOBILE = ModelFramework("tfmobile", ".pb", TensorFlowMobileFile)
CORE_ML = ModelFramework("coreml", ".mlmodel", CoreMLFile)
KERAS = ModelFramework("keras", ".h5", KerasFile)


def all_frameworks():
    """List of all supported frameworks.

    Returns: List[ModelFramework]
    """
    return [TENSORFLOW_LITE, TENSORFLOW_MOBILE, CORE_ML, KERAS]


def get_from_filename(filename):
    """Gets the corresponding `ModelFramework` from a filename.

    Args:
        filename (str): Filename.

    Returns: Framework if it is supported.
    """
    for framework in all_frameworks():
        if filename.endswith(framework.extension):
            return framework

    return None


def build_framework_file(path):
    """Builds the framework file from path.

    Args:
        path (str): Path.

    Returns: FrameworkFileBase if it is supported.
    """
    framework = get_from_filename(path)
    if not framework:
        return None

    return framework.build_file(path)
