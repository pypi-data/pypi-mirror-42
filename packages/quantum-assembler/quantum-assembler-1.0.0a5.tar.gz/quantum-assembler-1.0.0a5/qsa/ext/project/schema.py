import marshmallow
import marshmallow.fields

from qsa.schema import Schema


class ProjectConfigSchema(Schema):
    name = marshmallow.fields.String(missing=None, allow_none=True)
    type = marshmallow.fields.String(
        validate=[marshmallow.validate.OneOf(['application','library', 'k8s'])]
    )
    language = marshmallow.fields.String(required=False, allow_none=True,
        missing=None)


class ConfigSchema(Schema):
    project = marshmallow.fields.Nested(ProjectConfigSchema,
        missing=ProjectConfigSchema.defaults)
