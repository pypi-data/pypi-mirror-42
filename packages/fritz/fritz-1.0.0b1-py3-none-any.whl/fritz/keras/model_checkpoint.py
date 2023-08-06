"""
fritz.keras.model_checkpoint
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module contains a Keras callback to upload new versions of a
model to Fritz.
"""
import logging

import keras

import fritz

_logger = logging.getLogger(__name__)


class FritzSnapshotCallback(keras.callbacks.Callback):
    """Keras callback to create a ModelSnapshot in Fritz.

    Adding this callback will convert and upload mobile-ready models
    during training.
    """

    def __init__(self,
                 api_key=None,
                 project_uid=None,
                 model_uids_by_framework=None,
                 converters_by_framework=None,
                 output_file_name=None,
                 period=1,
                 deploy=False):
        """Save a Fritz Snapshot to Fritz.

        Args:
            api_key (Optional[str]): Optional API Key.
            project_uid (Optional[str]): Optional project uid, required if not
                globally set.
            converters_by_framework (Dict[frameworks.ModelFramework,
                (keras.model.Model) -> io.BytesIO): Dictionary mapping model
                framework to conversion function.
            model_uids_by_framework (Dict[frameworks.ModelFramework:str):
                Dictionary mapping model framework to model uids.  If model_uid
                not set for a given platform, a new model will be created.
            output_file_name (str): Name of output_file.
            period (int): Interval (number of epochs) between checkpoints.
            deploy (bool): If True will set active version of model to latest
                uploaded model. Default False.
        """
        super(FritzSnapshotCallback, self).__init__()
        self._api_key = api_key
        self._project_uid = project_uid
        self._output_file_name = output_file_name
        self._period = period
        self._deploy = deploy
        self._model_uids = model_uids_by_framework or {}
        self._converters = converters_by_framework or {}

    def add_model_metadata(self, logs):  # noqa pylint: disable=unused-argument,no-self-use
        """Adds additional metadata about the model to be stored in Fritz.

        Optionally override this method returning custom information.

        Args:
            logs (dict): Includes values such as `acc` and `loss`.

        Returns: Dict of model metadata.
        """
        return {}

    def on_epoch_end(self, epoch, logs=None):
        """Saves model to Fritz on epoch end.

        Args:
            epoch (int): the epoch number
            logs (dict, optional): logs dict
        """
        is_last_epoch = self.params.get('epochs') == epoch
        # Adding one so that the very first run does not trigger an upload.
        # If you specify period to be 3, the first upload will be on the 3rd
        # epoch.
        if not is_last_epoch and (epoch + 1) % self._period != 0:
            return

        _logger.info('Creating ModelSnapshot - epoch %s', epoch)
        metadata = {
            'epoch': epoch,
            'keras_model_path': self._output_file_name,
        }
        metadata.update(logs or {})
        metadata.update(self.add_model_metadata(logs))
        _, _, models = fritz.ModelSnapshot.create(
            api_key=self._api_key,
            project_uid=self._project_uid,
            output_filename=self._output_file_name,
            keras_model=self.model,
            set_active=self._deploy,
            metadata=metadata,
            converters=self._converters,
            model_uids=self._model_uids,
        )

        # Update previously unset model_uids with created models.
        for model in models:
            if not self._model_uids.get(model.framework):
                self._model_uids[model.framework] = model.uid
