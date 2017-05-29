from rest_framework.serializers import BaseSerializer, ValidationError

from marshmallow import Schema as MarshmallowSchema
from marshmallow import fields  # noqa

__version__ = '3.0.0'

_schema_kwargs = (
    'only', 'exclude', 'dump_only', 'load_only'
)


class Schema(BaseSerializer, MarshmallowSchema):
    def __init__(self, *args, **kwargs):
        schema_kwargs = {
            'many': kwargs.get('many', False)
        }
        # Remove any kwargs that are only valid for marshmallow schemas
        for key in _schema_kwargs:
            if key in kwargs:
                schema_kwargs[key] = kwargs.pop(key)

        super(Schema, self).__init__(*args, **kwargs)
        MarshmallowSchema.__init__(self, **schema_kwargs)

    def to_representation(self, instance):
        return self.dump(instance).data

    def to_internal_value(self, data):
        ret = self.load(data)
        if ret.errors:
            raise ValidationError(ret.errors)
        return ret.data

    @property
    def data(self):
        # We're overriding the default implementation here, because the
        # '_data' property clashes with marshmallow's implementation.
        if hasattr(self, 'initial_data') and not hasattr(self, '_validated_data'):
            msg = (
                'When a serializer is passed a `data` keyword argument you '
                'must call `.is_valid()` before attempting to access the '
                'serialized `.data` representation.\n'
                'You should either call `.is_valid()` first, '
                'or access `.initial_data` instead.'
            )
            raise AssertionError(msg)

        if not hasattr(self, '_serializer_data'):
            if self.instance is not None and not getattr(self, '_errors', None):
                self._serializer_data = self.to_representation(self.instance)
            elif hasattr(self, '_validated_data') and not getattr(self, '_errors', None):
                self._serializer_data = self.to_representation(self.validated_data)
            else:
                self._serializer_data = self.get_initial()
        return self._serializer_data

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, value):
        self._context = value

    get_attribute = MarshmallowSchema.get_attribute
