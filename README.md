# server

```sh
# create a virtual environement (recommended)
virtualenv env
source env/bin/activate 

# install the packages
pip install -r requirements.txt

# apply migrations
python manage.py makemigrations
python manage.py migrate

# create a user (admin), optional if you just want to use the default script
python manage.py createsuperuser

# default script
python manage.py < scripts/init.py

# run the server
python manage.py runserver

# run the server (optional : with a working websocket)
docker run -p 6379:6379 -d redis:5
python manage.py runserver

# launch the unit tests
python manage.py test
```
