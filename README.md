## Milton Web Server

### Configuration
To set up the environment, do these things:
1. .env file in the project root directory, containing variables
    * AWS_ACCESS_KEY_ID
    * AWS_SECRET_ACCESS_KEY
    * DJANGO_SETTINGS_MODULE
    * AWS_STORAGE_BUCKET_NAME
    * TEST_MEDIA
2.  Run `pipenv install` in the project root directory
3.  Run `brew install libmagic`
4.  Run
```
pipenv shell
python manage.py makemigrations
python manage.py migrate
```
 in the project root directory. If asked to set defaults for fields, do so.

