def pytest_configure():
    from django.conf import settings

    settings.configure()

    try:
        import django
        django.setup()
    except AttributeError:
        pass
