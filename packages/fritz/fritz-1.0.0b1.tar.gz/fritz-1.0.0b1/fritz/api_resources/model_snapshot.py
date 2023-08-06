"""
fritz.api_resources.model_snapshot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: © 2019 by Fritz Labs Incorporated
:license: MIT, see LICENSE for more details.
"""
import logging

import fritz
from fritz.api_resources.fritz_object import FritzObject
from fritz import frameworks

# pylint: disable=invalid-name
_logger = logging.getLogger(__name__)


class ModelSnapshot(FritzObject):
    """A collection of models built from the same training model. """
    OBJECT_NAME = 'ModelSnapshot'

    @classmethod
    def create(cls,
               api_key=None,
               project_uid=None,
               keras_model=None,
               converters=None,
               model_uids=None,
               output_filename=None,
               set_active=None,
               metadata=None):
        """Create new ModelSnapshot from a Keras model.

        Calling create will run all provided converters on `keras_model`
        and upload them to the API. All models will be bundled into
        the same ModelSnapshot

        Args:
            api_key (Optional[str]): API Key. Optional if `fritz.configure`
                was called.
            project_uid (Optional[str]): Project UID. Optional if
                `fritz.configure` was called with project_uid.
            keras_model (keras.models.Model): Keras Model.
            converters (Dict[frameworks.ModelFramework:(keras.model.Model) ->
                io.BytesIO): Dictionary mapping model framework to conversion
                function.
            model_uids (Dict[frameworks.ModelFramework:str): Dictionary mapping
                model framework to model uids.  If model_uid not set for a
                given platform, a new model will be created.
            output_filename (str): Name of Keras model output filename.
            set_active (bool): If True, model will be set as the active version
               in Fritz. If it is True, any devices runninng this model will
               download the latest version.
            metadata (dict): Dictionary of metadata.

        Returns: Tuple[fritz.ModelSnapshot, List[fritz.ModelVersion],
            List[fritz.Model]]
        """
        keras_file = frameworks.KerasFile(keras_model)
        model_uids = model_uids or {}
        versions = []
        models = []

        keras_model_uid = model_uids.get(frameworks.Frameworks.KERAS)
        version, snapshot, model = fritz.ModelVersion.create(
            api_key=api_key,
            project_uid=project_uid,
            filename=output_filename,
            data=keras_file.to_bytes(),
            model_uid=keras_model_uid,
            set_active=set_active,
            metadata=metadata,
        )
        versions.append(version)
        models.append(model)

        for framework, converter in converters.items():
            _logger.info('Converting %s model', framework.name)

            converted_model = converter(keras_model)
            framework_file = framework.to_file(converted_model)

            version, snapshot, _ = fritz.ModelVersion.create(
                api_key=api_key,
                project_uid=project_uid,
                model_uid=model_uids.get(framework),
                snapshot_uid=snapshot.uid,
                filename=framework.as_framework_filename(output_filename),
                data=framework_file.to_bytes(),
                set_active=set_active,
                metadata=metadata,
            )
            versions.append(version)

        return snapshot, versions, models
