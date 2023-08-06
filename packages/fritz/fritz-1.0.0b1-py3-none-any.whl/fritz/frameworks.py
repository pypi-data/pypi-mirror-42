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


class FrameworkFileBase(object):
    """Base class to wrap models for interacting with Fritz."""

    def __init__(self, framework, model):
        self.framework = framework
        self.model = model

    def to_bytes(self):
        """Convert model to bytes.

        Returns: io.BytesIO object
        """
        raise NotImplementedError("Super class must implement")


class KerasFile(FrameworkFileBase):
    """Wrapper class for Keras model."""

    def __init__(self, model):
        super(KerasFile, self).__init__(Frameworks.KERAS, model)

    def to_bytes(self):
        # need to actually get the bytes here.
        tmp_file = tempfile.NamedTemporaryFile()
        self.model.save(tmp_file.name)
        tmp_file.seek(0)

        return tmp_file.read()


class CoreMLFile(FrameworkFileBase):
    """Wrapper class for Core ML model."""

    def __init__(self, model):
        super(CoreMLFile, self).__init__(Frameworks.CORE_ML, model)

    def to_bytes(self):
        serialized_spec = self.model.get_spec().SerializeToString()
        return io.BytesIO(serialized_spec)


class TensorFlowLiteFile(FrameworkFileBase):
    """Wrapper class for TensorFlow Lite model."""

    def __init__(self, model):
        super(TensorFlowLiteFile, self).__init__(Frameworks.TENSORFLOW_LITE,
                                                 model)

    def to_bytes(self):
        return io.BytesIO(self.model)


class TensorFlowMobileFile(FrameworkFileBase):
    """Wrapper class for TensorFlow Mobile model."""

    def __init__(self, model):
        super(TensorFlowMobileFile, self).__init__(
            Frameworks.TENSORFLOW_MOBILE, model)

    def to_bytes(self):
        return io.BytesIO(self.model)


class Frameworks(object):
    """Collection of supported Frameworks"""

    TENSORFLOW_LITE = ModelFramework('tflite', '.tflite', TensorFlowLiteFile)
    TENSORFLOW_MOBILE = ModelFramework('tfmobile', '.pb', TensorFlowMobileFile)
    CORE_ML = ModelFramework('coreml', '.mlmodel', CoreMLFile)
    KERAS = ModelFramework('keras', '.h5', KerasFile)

    @classmethod
    def all_frameworks(cls):
        """List of all supported frameworks.

        Returns: List[ModelFramework]
        """
        return [
            cls.TENSORFLOW_LITE,
            cls.TENSORFLOW_MOBILE,
            cls.CORE_ML,
            cls.KERAS,
        ]

    @classmethod
    def get_from_filename(cls, filename):
        """Gets the corresponding `ModelFramework` from a filename.

        Args:
            filename (str): Filename.

        Returns: Framework if it is supported.
        """
        for framework in cls.all_frameworks():
            if filename.endswith(framework.extension):
                return framework

        return None
