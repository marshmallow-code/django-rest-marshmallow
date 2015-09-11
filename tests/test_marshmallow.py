from marshmallow import Schema, fields
from rest_marshmallow import create_serializer_class


class Object(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class ExampleSchema(Schema):
    number = fields.Integer()
    text = fields.String()


ExampleSerializer = create_serializer_class(ExampleSchema)


def test_serialize():
    instance = Object(number=123, text='abc')
    serializer = ExampleSerializer(instance)
    assert serializer.data == {'number': 123, 'text': 'abc'}


def test_serialize_many():
    instances = [Object(number=123, text='abc') for i in range(3)]
    serializer = ExampleSerializer(instances, many=True)
    assert serializer.data == [
        {'number': 123, 'text': 'abc'},
        {'number': 123, 'text': 'abc'},
        {'number': 123, 'text': 'abc'},
    ]


def test_deserialize():
    data = {'number': 123, 'text': 'abc'}
    serializer = ExampleSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data == {'number': 123, 'text': 'abc'}


def test_deserialize_validation_failed():
    data = {'number': 'abc', 'text': 'abc'}
    serializer = ExampleSerializer(data=data)
    assert not serializer.is_valid()
    assert serializer.errors == {
        'number': ["invalid literal for int() with base 10: 'abc'"]
    }
