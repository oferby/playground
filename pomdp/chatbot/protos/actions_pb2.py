# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: actions.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='actions.proto',
  package='actions',
  syntax='proto3',
  serialized_options=_b('\n\027com.huawei.ibcs.actionsB\013ActionProtoP\001\242\002\003HLW'),
  serialized_pb=_b('\n\ractions.proto\x12\x07\x61\x63tions\"\x8c\x01\n\x12\x43loudActionRequest\x12\x0e\n\x06\x61\x63tion\x18\x01 \x01(\t\x12\x37\n\x06params\x18\x02 \x03(\x0b\x32\'.actions.CloudActionRequest.ParamsEntry\x1a-\n\x0bParamsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\'\n\x13\x43loudActionResponse\x12\x10\n\x08response\x18\x01 \x03(\t2^\n\x12\x43loudActionService\x12H\n\tgetAction\x12\x1b.actions.CloudActionRequest\x1a\x1c.actions.CloudActionResponse\"\x00\x42.\n\x17\x63om.huawei.ibcs.actionsB\x0b\x41\x63tionProtoP\x01\xa2\x02\x03HLWb\x06proto3')
)




_CLOUDACTIONREQUEST_PARAMSENTRY = _descriptor.Descriptor(
  name='ParamsEntry',
  full_name='actions.CloudActionRequest.ParamsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='actions.CloudActionRequest.ParamsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='actions.CloudActionRequest.ParamsEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=122,
  serialized_end=167,
)

_CLOUDACTIONREQUEST = _descriptor.Descriptor(
  name='CloudActionRequest',
  full_name='actions.CloudActionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='action', full_name='actions.CloudActionRequest.action', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='params', full_name='actions.CloudActionRequest.params', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_CLOUDACTIONREQUEST_PARAMSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=27,
  serialized_end=167,
)


_CLOUDACTIONRESPONSE = _descriptor.Descriptor(
  name='CloudActionResponse',
  full_name='actions.CloudActionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='response', full_name='actions.CloudActionResponse.response', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=169,
  serialized_end=208,
)

_CLOUDACTIONREQUEST_PARAMSENTRY.containing_type = _CLOUDACTIONREQUEST
_CLOUDACTIONREQUEST.fields_by_name['params'].message_type = _CLOUDACTIONREQUEST_PARAMSENTRY
DESCRIPTOR.message_types_by_name['CloudActionRequest'] = _CLOUDACTIONREQUEST
DESCRIPTOR.message_types_by_name['CloudActionResponse'] = _CLOUDACTIONRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CloudActionRequest = _reflection.GeneratedProtocolMessageType('CloudActionRequest', (_message.Message,), dict(

  ParamsEntry = _reflection.GeneratedProtocolMessageType('ParamsEntry', (_message.Message,), dict(
    DESCRIPTOR = _CLOUDACTIONREQUEST_PARAMSENTRY,
    __module__ = 'actions_pb2'
    # @@protoc_insertion_point(class_scope:actions.CloudActionRequest.ParamsEntry)
    ))
  ,
  DESCRIPTOR = _CLOUDACTIONREQUEST,
  __module__ = 'actions_pb2'
  # @@protoc_insertion_point(class_scope:actions.CloudActionRequest)
  ))
_sym_db.RegisterMessage(CloudActionRequest)
_sym_db.RegisterMessage(CloudActionRequest.ParamsEntry)

CloudActionResponse = _reflection.GeneratedProtocolMessageType('CloudActionResponse', (_message.Message,), dict(
  DESCRIPTOR = _CLOUDACTIONRESPONSE,
  __module__ = 'actions_pb2'
  # @@protoc_insertion_point(class_scope:actions.CloudActionResponse)
  ))
_sym_db.RegisterMessage(CloudActionResponse)


DESCRIPTOR._options = None
_CLOUDACTIONREQUEST_PARAMSENTRY._options = None

_CLOUDACTIONSERVICE = _descriptor.ServiceDescriptor(
  name='CloudActionService',
  full_name='actions.CloudActionService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=210,
  serialized_end=304,
  methods=[
  _descriptor.MethodDescriptor(
    name='getAction',
    full_name='actions.CloudActionService.getAction',
    index=0,
    containing_service=None,
    input_type=_CLOUDACTIONREQUEST,
    output_type=_CLOUDACTIONRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_CLOUDACTIONSERVICE)

DESCRIPTOR.services_by_name['CloudActionService'] = _CLOUDACTIONSERVICE

# @@protoc_insertion_point(module_scope)
