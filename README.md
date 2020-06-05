## Orange is the new back

A CRUD backend to orange app based on Django 3.0, cors and graphene-django.

### `pip install -r requirements.txt`

Installs all necessary packages to run the project.

### `python manage.py makemigrations`
Prepare all the necessary tables to migrations.
 
### `python manage.py migrate`
Create all the neccessary tables in a database of your choosing.

### `python manage.py createsuperuser`
Create one if you want to access all the data in the admin site.

#### `python manage.py runserver`
Get you project running.


# Things to remember:
Place 'corsheaders.middleware.CorsMiddleware' right after 'django.contrib.sessions.middleware.SessionMiddleware' in the MIDDLEWARE section of your settings.py

Equip AUTHENTICATION_BACKENDS with 'graphql_jwt.backends.JSONWebTokenBackend'. Place it on the top.

Last but definitely not least:
paste:
`GRAPHENE = {
    'SCHEMA': 'orange_app_back.schema.schema'
}`

and
`CORS_ORIGIN_WHITELIST = (
    'http://your_frontend_url:port',
)`

and the bottom of your settings.py
