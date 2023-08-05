# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ScheduleCreationInfo(Model):
    """ScheduleCreationInfo.

    :param name:
    :type name: str
    :param pipeline_id:
    :type pipeline_id: str
    :param pipeline_submission_info:
    :type pipeline_submission_info: ~swagger.models.PipelineSubmissionInfo
    :param recurrence:
    :type recurrence: ~swagger.models.Recurrence
    """

    _attribute_map = {
        'name': {'key': 'Name', 'type': 'str'},
        'pipeline_id': {'key': 'PipelineId', 'type': 'str'},
        'pipeline_submission_info': {'key': 'PipelineSubmissionInfo', 'type': 'PipelineSubmissionInfo'},
        'recurrence': {'key': 'Recurrence', 'type': 'Recurrence'},
    }

    def __init__(self, name=None, pipeline_id=None, pipeline_submission_info=None, recurrence=None):
        super(ScheduleCreationInfo, self).__init__()
        self.name = name
        self.pipeline_id = pipeline_id
        self.pipeline_submission_info = pipeline_submission_info
        self.recurrence = recurrence
