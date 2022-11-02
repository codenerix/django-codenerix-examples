Basic
=====

# Django Codenerix  Examples - Basic with double GenList over the same model

*Basic Double GenList* extends the example *Basic* with an extra GenList pointing to the same model.

You can aproach this setting 'modelname' and 'appname' attributes in your custom GenList.


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
