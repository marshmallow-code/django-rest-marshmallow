from rest_framework.serializers import BaseSerializer, ValidationError


__version__ = '1.0.0'


def create_serializer_class(schema_class):
    return type('Test', (MarshmallowSerializer,), {'_schema_class': schema_class})


class MarshmallowSerializer(BaseSerializer):
    def __init__(self, *args, **kwargs):
        super(MarshmallowSerializer, self).__init__(*args, **kwargs)
        self._schema = self._schema_class(many=kwargs.get('many', False))

    def to_representation(self, instance):
        return self._schema.dump(instance).data

    def to_internal_value(self, data):
        ret = self._schema.load(data)
        if ret.errors:
            raise ValidationError(ret.errors)
        return ret.data
