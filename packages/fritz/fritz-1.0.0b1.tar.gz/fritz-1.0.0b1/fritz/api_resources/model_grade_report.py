"""
fritz.api_resources.model_grade_report
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: © 2019 by Fritz Labs Incorporated
:license: MIT, see LICENSE for more details.
"""

import fritz
from fritz.api_resources import fritz_object
from fritz.api_client import FritzClient


class ModelGradeReport(fritz_object.FritzObject):
    """Model Benchmark report."""

    OBJECT_NAME = 'ModelGradeReport'

    @classmethod
    def get(cls, version_uid, api_key=None):
        """Get model grade report for version_uid

        Args:
            version_uid (str): UID of ModelVersion
            api_key (str): Optional API Key

        Returns: ModelGradeReport if report has succeeded.
        """
        url = '/model/version/{version_uid}/grader'.format(
            version_uid=version_uid)

        client = FritzClient(api_key or fritz.api_key)
        response = client.get(url)
        return fritz.utils.convert_to_fritz_object(response)
