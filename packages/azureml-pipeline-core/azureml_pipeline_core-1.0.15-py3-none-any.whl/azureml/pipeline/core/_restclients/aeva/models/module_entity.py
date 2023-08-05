# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ModuleEntity(Model):
    """ModuleEntity.

    :param module_execution_type:
    :type module_execution_type: str
    :param upload_state: Possible values include: 'Uploading', 'Completed',
     'Canceled', 'Failed'
    :type upload_state: str or ~swagger.models.enum
    :param is_deterministic:
    :type is_deterministic: bool
    :param structured_interface:
    :type structured_interface: ~swagger.models.StructuredInterface
    :param data_location:
    :type data_location: ~swagger.models.DataLocation
    :param identifier_hash:
    :type identifier_hash: str
    :param name:
    :type name: str
    :param hash:
    :type hash: str
    :param description:
    :type description: str
    :param id:
    :type id: str
    :param etag:
    :type etag: str
    :param created_date:
    :type created_date: datetime
    :param last_modified_date:
    :type last_modified_date: datetime
    :param entity_status: Possible values include: 'Active', 'Deprecated',
     'Disabled'
    :type entity_status: str or ~swagger.models.enum
    """

    _attribute_map = {
        'module_execution_type': {'key': 'ModuleExecutionType', 'type': 'str'},
        'upload_state': {'key': 'UploadState', 'type': 'str'},
        'is_deterministic': {'key': 'IsDeterministic', 'type': 'bool'},
        'structured_interface': {'key': 'StructuredInterface', 'type': 'StructuredInterface'},
        'data_location': {'key': 'DataLocation', 'type': 'DataLocation'},
        'identifier_hash': {'key': 'IdentifierHash', 'type': 'str'},
        'name': {'key': 'Name', 'type': 'str'},
        'hash': {'key': 'Hash', 'type': 'str'},
        'description': {'key': 'Description', 'type': 'str'},
        'id': {'key': 'Id', 'type': 'str'},
        'etag': {'key': 'Etag', 'type': 'str'},
        'created_date': {'key': 'CreatedDate', 'type': 'iso-8601'},
        'last_modified_date': {'key': 'LastModifiedDate', 'type': 'iso-8601'},
        'entity_status': {'key': 'EntityStatus', 'type': 'str'},
    }

    def __init__(self, module_execution_type=None, upload_state=None, is_deterministic=None, structured_interface=None, data_location=None, identifier_hash=None, name=None, hash=None, description=None, id=None, etag=None, created_date=None, last_modified_date=None, entity_status=None):
        super(ModuleEntity, self).__init__()
        self.module_execution_type = module_execution_type
        self.upload_state = upload_state
        self.is_deterministic = is_deterministic
        self.structured_interface = structured_interface
        self.data_location = data_location
        self.identifier_hash = identifier_hash
        self.name = name
        self.hash = hash
        self.description = description
        self.id = id
        self.etag = etag
        self.created_date = None
        self.last_modified_date = None
        self.entity_status = entity_status
