"""
fritz.api_resources.model_version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: © 2019 by Fritz Labs Incorporated
:license: MIT, see LICENSE for more details.
"""
import time
import logging

import fritz
import fritz.utils
import fritz.errors
from fritz.api_resources.fritz_object import FritzObject
from fritz.api_client import FritzClient

_logger = logging.getLogger(__name__)


class ModelVersion(FritzObject):
    """ModelVersion  """
    OBJECT_NAME = 'ModelVersion'

    @classmethod
    def create(cls,
               api_key=None,
               project_uid=None,
               model_uid=None,
               snapshot_uid=None,
               filename=None,
               data=None,
               set_active=None,
               metadata=None):
        """Create a new ModelVersion, uploading file to Fritz.

        Args:
            api_key (Optional[str]): API Key. Optional if `fritz.configure`
                was called.
            project_uid (Optional[str]): Project UID. Optional if
                `fritz.configure` was called with project_uid.
            model_uid (str): optional Model UID.
            snapshot_uid (str): If snapshot_uid set, will attach version to
                given snapshot.
            filename (str): Name of model version filename.
            set_active (bool): If True, model will be set as the active version
               in Fritz. If it is True, any devices runninng this model will
               download the latest version.
            metadata (dict): Dictionary of metadata.

        Returns:
            Tuple[ModelVersion, ModelSnapshot, Model]
        """
        if not fritz.api_key and not api_key:
            raise fritz.errors.FritzNotInitializedError()

        if model_uid:
            url = '/model/{model_uid}/version'.format(model_uid=model_uid)
        else:
            url = '/model/version'

        client = FritzClient(api_key or fritz.api_key)
        response = client.post(
            url,
            params={
                'project_uid': project_uid or fritz.project_uid,
                'snapshot_uid': snapshot_uid,
                'model_uid': model_uid,
            },
            data={
                'set_active': set_active,
                'metadata': metadata,
            },
            files={
                'file': (filename, data),
            }
        )
        converted = {key: fritz.utils.convert_to_fritz_object(value)
                     for key, value in response.items()}
        return converted['version'], converted['snapshot'], converted['model']

    @classmethod
    def get(cls, version_uid, api_key=None):
        """Get version by version_uid

        Args:
            version_uid: Version UID
            api_key (str): Optional API Key to use.

        Returns: ModelVersion
        """
        url = '/model/version/{version_uid}'.format(
            version_uid=version_uid)

        client = FritzClient(api_key or fritz.api_key)

        response = client.get(url)
        return fritz.utils.convert_to_fritz_object(response)

    def benchmark(self,
                  api_key=None,
                  wait_seconds=5,
                  attempts=5):
        """Get model grade report, waiting if it does not yet exist.

        Args:
            api_key (str): Optional API Key
            wait_seconds (int): Number of seconds to wait between each
                request.
            attempts (int): Number of attempts to make.

        Returns: ModelGradeReport if it exists
        """

        try:
            return fritz.ModelGradeReport.get(self.uid, api_key=api_key)
        except fritz.errors.FritzError as err:
            if err.status_code != 404:
                raise err
            _logger.info('Grader report not found, trying again')
            attempts -= 1
            if attempts < 0:
                raise err

            time.sleep(wait_seconds)

            return self.benchmark(
                api_key=api_key,
                wait_seconds=wait_seconds,
                attempts=attempts
            )
