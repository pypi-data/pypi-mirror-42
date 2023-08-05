# django-rest-framework-kong-consumers

Kong consumers for Django


## Instructions

1. Add "django_rest_framework_kong_consumers" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_rest_framework_kong_consumers',
    ]
    
2. Set the default django user model and setup rest authentication in settings file::

    AUTH_USER_MODEL = 'django_rest_framework_kong_consumers.Consumer'

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'django_rest_framework_kong_consumers.authentication.KongConsumerAuthentication'
        ],
        ...
    
3. Include the django_rest_framework_kong_consumers URLconf in your project urls.py like this::
    
    from django_rest_framework_kong_consumers.urls import urlpatterns as consumers_urls

    urlpatterns = [
        ...
        url(r'^api/v1/consumers/', include(consumers_urls)),
    ]

4. Run `python manage.py migrate` to create the django_rest_framework_kong_consumers models.

5. Visit http://127.0.0.1:8000/api/v1/consumers/consumers/ to list consumers.

5. Visit http://127.0.0.1:8000/api/v1/consumers/groups/ to list consumers.



## Note

This project has been set up using PyScaffold 3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
