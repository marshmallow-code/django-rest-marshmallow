<div class="badges">
    <a href="http://travis-ci.org/marshmallow-code/django-rest-marshmallow">
        <img src="https://travis-ci.org/marshmallow-code/django-rest-marshmallow.svg?branch=master">
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

* Python (3.6+)
* Django REST framework (3.8+)
* Marshmallow (3.0.0+)

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

    class CustomerListView(generics.ListAPIView):
        queryset = Customer.objects.all()
        serializer_class = CustomerSchema

Or use the serializer API directly, for either serialization...

    serializer = CustomerSchema(queryset, many=True)
    return Response(serializer.data)

Or for validation...

    serializer = CustomerSchema(data=request.data)
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

    serializer = CustomerSchema(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

Or use the schema together with generic views that create or update instances...

    class CustomerListView(generics.ListCreateAPIView):
        queryset = Customer.objects.all()
        serializer_class = CustomerSchema

Note that you should always use the `create()` and `update()` methods instead of overriding the `make_object()` marshmallow method.

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

    serializer = CustomerSchema(queryset, many=True, only=('name', 'email'))
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

## Changelog

### 5.0.0 (unreleased)

* Drop support for Python 2 and marshmallow 2.
  Only Python>=3.6 and marshmallow>=3 are supported.

### 4.0.2 (2020-03-19)

* Fix serializing `Date` field
([#110](https://github.com/marshmallow-code/django-rest-marshmallow/issues/110) and [#131](https://github.com/marshmallow-code/django-rest-marshmallow/issues/131)).
Thanks [@michaelwiles](https://github.com/michaelwiles) for the fix.

### 4.0.1 (2019-07-30)

* Allow passing `partial` to constructor ([#103](https://github.com/marshmallow-code/django-rest-marshmallow/issues/103)).
  Thanks [@davidzwa](https://github.com/davidzwa) for the catch and patch.

### 4.0.0 (2019-02-14)

* Drop official support for Python 3.4. Only Python 2.7 and >= 3.5 are supported.
* Officially support django-rest-framework>=3.8.
* Officially support marshmallow>=2.15.3 and >=3.0.0b18.
* Fix behavior when passing `many=True` to a `Nested` field ([#72](https://github.com/marshmallow-code/django-rest-marshmallow/issues/72)). Thanks [@tyhoff](https://github.com/tyhoff)
  for reporting and thanks [@droppoint](https://github.com/marshmallow-code/django-rest-marshmallow/pull/75) for the PR.

### 3.1.1 (2018-05-24)

* Support passing `context` argument ([#17](https://github.com/marshmallow-code/django-rest-marshmallow/issues/17)). Thanks [@pablotrinidad](https://github.com/pablotrinidad) for reporting
 and thanks [@dhararon](https://github.com/dhararon) for the PR.

### 3.1.0 (2018-02-11)

* Support marshmallow>=3.0.0b7. Thanks [@trnsnt](https://github.com/trnsnt).

### 3.0.0 (2017-05-29)

* Officially support Python 3.6.
* Fix error thrown when using a `Nested` field ([#12](https://github.com/marshmallow-code/django-rest-marshmallow/issues/12)). Thanks [@devashishsharma2302](https://github.com/devashishsharma2302) for the fix.
* Drop support for Django<1.10 and DRF<3.4.

### 2.0.0 (2016-10-09)

* Drop support for marshmallow 1.x. Only marshmallow>=2.0.0 is supported.
* Officially support Python 3.4 and 3.5.
* Drop support for Python 3.3 (which is no longer supported by Django).

### 1.0.1 (2016-10-02)

* Fix bug that raised a ``TypeError`` on serialization ([#6](https://github.com/marshmallow-code/django-rest-marshmallow/issues/6)).

### 1.0.0 (2015-09-11)

* First release.

[marshmallow]: https://marshmallow.readthedocs.org/en/latest/
