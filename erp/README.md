# Django Codenerix  Examples - ERP

*ERP* is the most advanced application we have done so far to manage many aspects from a company (Products, Bills, Stock, Shopping online, Point-of-Sale, Website, Mailing and Payments). It was designed to use all the modules available at **[CODENERIX](https://github.com/codenerix)**


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

6. Apply all migrations::
```
   ./manage.py migrate
```

7. Create a superuser::
```
    ./manage.py createsuperuser
```

8. Launch the backend::
```
    ./manage.py runserver backend
```


## Extras

If you would like to launche several environments you may use the port number after the choosen environment, example::

```
    ./manage.py runserver backend          # It will start backend on port 8000
    ./manage.py runserver frontend 8001    # It will start frontend on port 8001
```

## About the authors
- **Name:** Juanmi Taboada
- **E-Mail:** juanmi@juanmitaboada.com
- **GitHub:** https://github.com/juanmitaboada

- **Name:** Juan Soler
- **E-Mail:** soleronline@gmail.com
- **GitHub:** https://github.com/soleronline
