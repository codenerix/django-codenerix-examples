Basic
=====

# Django Codenerix  Examples - Basic

*Basic* is probably the most simple web application we have. It was designed as a startup project for a new **[CODENERIX](https://github.com/codenerix)** project.


## Installation

1. Create a database and a user for that database with enought privileges to create tables and apply all migrations

2. Configure database in erp/config.py (MySQL recommended)

3. Create an environment::
```
    virtualenv -p python3 env
```

4. Activate environment::
```
    source env/bin/activate
```

5. Install all required python packages::
```
    pip install -r requirements.txt
```

6. Create migrations::
```
   ./manage.py makemigrations
```

7. Apply migrations::
```
   ./manage.py migrate
```

8. Create a superuser::
```
    ./manage.py createsuperuser
```

9. Launch the server::
```
    ./manage.py runserver
```


## About the author

**Juanmi Taboada** <juanmi@juanmitaboada.com> - https://github.com/juanmitaboada
