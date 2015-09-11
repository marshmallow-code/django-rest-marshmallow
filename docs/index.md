<div class="badges">
    <a href="http://travis-ci.org/tomchristie/django-rest-marshmallow">
        <img src="https://travis-ci.org/tomchristie/django-rest-marshmallow.svg?branch=master">
    </a>
    <a href="https://pypi.python.org/pypi/django-rest-marshmallow">
        <img src="https://img.shields.io/pypi/v/django-rest-marshmallow.svg">
    </a>
</div>

---

# django-rest-marshmallow

[Marshmallow schemas][marshmallow] for Django REST framework.

---

## Overview

`django-rest-marshmallow` provides an alternative serializer implementation to the built-in serializers, by using the python [marshmallow] library, but exposing the same API as REST framework's `Serializer` class.

## Requirements

* Python (2.7, 3.3+)
* Django REST framework (3.0+)
* Marshmallow (1.2+, 2.0+)

## Installation

Install using `pip`...

```bash
$ pip install django-rest-marshmallow
```

---

## Usage

Define your schemas as you would with marshmallow, but importing the `Schema` class from `rest_marshmallow` instead.

    from rest_marshmallow import Schema, fields

    class CustomerSchema(Schema):
        name = fields.String()
        email = fields.Email()
        created_at = fields.DateTime()

The Schema class has the same interface as a Django REST framework serializer, so you can use it in your generic views...

    serializer_class = CustomerSerializer

Or use the serializer API directly, for either serialization...

    serializer = CustomerSerializer(queryset, many=True)
    return Response(serializer.data)

Or for validation...

    serializer = CustomerSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.validated_data

#### Instance create and update

If you want to support `serializer.save()` you'll need to define the `.create()` and/or `.update()` methods explicitly.

    class CustomerSchema(Schema):
        name = fields.String()
        email = fields.Email()
        created_at = fields.DateTime()

        def create(self, validated_data):
            return Customer.objects.create(**validated_data)

        def update(self, instance, validated_data):
            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save()
            return instance

You can now use `.save()` from your view code…

    serializer = CustomerSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

You should use these methods instead of overriding the `make_object()` marshmallow method.

#### Nested representations

For nested representations, use marshmallow's standard `Nested` field as usual.

    from rest_marshmallow import fields, Schema

    class ArtistSchema(Schema):
        name = fields.String()

    class AlbumSchema(Schema):
        title = fields.String()
        release_date = fields.Date()
        artist = fields.Nested(ArtistSchema)

#### Excluding fields

The marshmallow `only` and `exclude` arguments are also valid as serializer arguments:

    serializer = CustomerSerializer(queryset, many=True, only=('name', 'email'))
    return Response(serializer.data)

---

## Testing

Install testing requirements.

```bash
$ pip install -r requirements.txt
```

Run with runtests.

```bash
$ ./runtests.py
```

You can also use the excellent [tox](http://tox.readthedocs.org/en/latest/) testing tool to run the tests against all supported versions of Python and Django. Install tox globally, and then simply run:

```bash
$ tox
```

## Documentation

To build the documentation, you'll need to install `mkdocs`.

```bash
$ pip install mkdocs
```

To preview the documentation:

```bash
$ mkdocs serve
Running at: http://127.0.0.1:8000/
```

To build the documentation:

```bash
$ mkdocs build
```


[marshmallow]: https://marshmallow.readthedocs.org/en/latest/
