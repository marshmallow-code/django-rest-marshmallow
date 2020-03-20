from datetime import date

from rest_marshmallow import Schema, fields


import marshmallow

IS_MARSHMALLOW_1 = marshmallow.__version__.split('.')[0] == '1'


class Object(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class ExampleSerializer(Schema):
    number = fields.Integer()
    text = fields.String()
    date = fields.Date()

    def create(self, validated_data):
        return Object(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        return instance


class NestedSerializer(Schema):
    top = fields.Integer()
    child = fields.Nested(ExampleSerializer)


class ManyNestedSerializer(Schema):
    top = fields.Integer()
    children = fields.Nested(ExampleSerializer, many=True)


def test_serialize():
    instance = Object(number=123, text='abc')
    serializer = ExampleSerializer(instance)
    assert serializer.data == {'number': 123, 'text': 'abc'}


def test_serialize_nested():
    instance = Object(top=1, child=Object(number=123, text='abc'))
    serializer = NestedSerializer(instance)
    assert serializer.data == {'top': 1, 'child': {'number': 123, 'text': 'abc'}}


def test_serialize_many():
    instances = [Object(number=123, text='abc') for i in range(3)]
    serializer = ExampleSerializer(instances, many=True)
    assert serializer.data == [
        {'number': 123, 'text': 'abc'},
        {'number': 123, 'text': 'abc'},
        {'number': 123, 'text': 'abc'},
    ]


def test_serialize_nested_many():
    instance = Object(top=1, children=[Object(number=123, text='abc') for i in range(3)])
    serializer = ManyNestedSerializer(instance)
    assert serializer.data == {'top': 1, 'children': [
        {'number': 123, 'text': 'abc'},
        {'number': 123, 'text': 'abc'},
        {'number': 123, 'text': 'abc'},
    ]}


def test_serialize_only():
    instance = Object(number=123, text='abc', date=date.today())
    serializer = ExampleSerializer(instance, only=('text',))
    assert serializer.data == {'text': 'abc'}


def test_deserialize():
    data = {'number': 123, 'text': 'abc'}
    serializer = ExampleSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data == {'number': 123, 'text': 'abc'}


def test_deserialize_validation_failed():
    data = {'number': 'abc', 'text': 'abc'}
    serializer = ExampleSerializer(data=data)
    assert not serializer.is_valid()
    if IS_MARSHMALLOW_1:
        expected_error = "invalid literal for int() with base 10: 'abc'"
    else:
        expected_error = 'Not a valid integer.'

    assert serializer.errors == {
        'number': [expected_error]
    }


def test_create():
    data = {'number': 123, 'text': 'abc'}
    serializer = ExampleSerializer(data=data)
    assert serializer.is_valid()
    instance = serializer.save()
    assert isinstance(instance, Object)
    assert instance.number == 123
    assert instance.text == 'abc'
    assert serializer.data == {'number': 123, 'text': 'abc'}


def test_update():
    instance = Object(number=123, text='abc')
    data = {'number': 456, 'text': 'def'}
    serializer = ExampleSerializer(instance, data=data)
    assert serializer.is_valid()
    serializer.save()
    assert instance.number == 456
    assert instance.text == 'def'
    assert serializer.data == {'number': 456, 'text': 'def'}


def test_context_data():
    instance = Object(number=123, text='abc')
    serializer = ExampleSerializer(instance, context={'test': 'data'})
    assert serializer.context == {'test': 'data'}
