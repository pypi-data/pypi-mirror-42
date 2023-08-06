"""
Fritz is a library to simplify your mobile machine learning workflow.

usage:
   >>> import fritz
   >>> client = fritz.client.FritzClient('<your api key>')
   >>> model_details = client.upload_new_model_version(
           '<model_uid>', '/path/to/your_great_model.mlmodel'
       )
   >>> print(model_details)
   {
       'model': {'uid': '<model_uid>', ...}
       'version': {'uid': '<version_uid>', ...}
   }

:copyright: © 2018 by Fritz Labs Incorporated
:license: MIT, see LICENSE for more details.
"""
# pylint: disable=invalid-name

from fritz.api_resources import *  # noqa

# Configuration Variables
api_key = None
project_uid = None
api_base = 'https://api.fritz.ai/client/v1'


def configure(**kwargs):
    """Sets Fritz configuration variables

    Args:
        api_key (str): Client API Key used to authenticate requests to Fritz.
        project_uid (str): Project UID to store models in.
        api_base (str): Base URL of Fritz API
    """
    # pylint: disable=global-statement
    global api_key, project_uid, api_base
    api_key = kwargs.get('api_key') or api_key
    project_uid = kwargs.get('project_uid') or project_uid
    api_base = kwargs.get('api_base') or api_base
