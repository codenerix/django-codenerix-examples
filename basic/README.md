Basic
=====

# Django Codenerix  Examples - Basic

*Basic* is probably the most simple web application we have. It was designed as a startup project for a new **[CODENERIX](https://github.com/codenerix)** project.


## Installation

1. Create an environment::
```
    virtualenv -p python3 env
```

2. Activate environment::
```
    source env/bin/activate
```

3. Install all required python packages::
```
    pip install -r requirements.txt
```

4. Create migrations::
```
   ./manage.py makemigrations
```

5. Apply migrations::
```
   ./manage.py migrate
```

6. Create a superuser::
```
    ./manage.py createsuperuser
```

7. Launch the server::
```
    ./manage.py runserver
```

8. Visit **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**


## About the author

**Juanmi Taboada** <juanmi@juanmitaboada.com> - https://github.com/juanmitaboada
