import marshmallow
from marshmallow import Schema as MarshmallowSchema
from marshmallow import fields  # noqa
from marshmallow.exceptions import ValidationError as MarshmallowValidationError
from rest_framework.serializers import BaseSerializer, ValidationError


IS_MARSHMALLOW_LT_3 = int(marshmallow.__version__.split('.')[0]) < 3


__version__ = '4.0.1'

_schema_kwargs = (
    'only', 'exclude', 'dump_only', 'load_only', 'context', 'partial'
)


class Schema(BaseSerializer, MarshmallowSchema):

    def __new__(cls, *args, **kwargs):
        # We're overriding the DRF implementation here, because ListSerializer
        # clashes with Nested implementation.
        kwargs.pop('many', False)
        return super(Schema, cls).__new__(cls, *args, **kwargs)

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
        if IS_MARSHMALLOW_LT_3:
            return self.dump(instance).data
        return self.dump(instance)

    def to_internal_value(self, data):
        if IS_MARSHMALLOW_LT_3:
            ret = self.load(data)
            if ret.errors:
                raise ValidationError(ret.errors)
            return ret.data
        try:
            return self.load(data)
        except MarshmallowValidationError as err:
            raise ValidationError(err.messages)

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
