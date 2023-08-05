import marshmallow
import marshmallow.fields

from qsa.schema import Schema


class ContainerConfigSchema(Schema):
    registry = marshmallow.fields.String(required=False,
        missing='docker.io')
    repository = marshmallow.fields.String(required=True)


class ConfigSchema(Schema):
    container = marshmallow.fields.Nested(ContainerConfigSchema,
        missing=ContainerConfigSchema.defaults)
