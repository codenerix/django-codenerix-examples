ERP
======

*ERP* is the most advanced application we have done so far to manage all kind of aspects from a company. I was designed to use all the features of **Codenerix**.


Installation
------------

- Create a database and a user for that database with enought privileges to create tables and apply all migrations
- Configure database in erp/config.py
- Create an environment: virtualenv -p python3 env
- Activate environment: source env/bin/activate
- Install all required python packages: pip install -r requirements.txt
- Apply all migrations: ./manage.py migrate
- Create a superuser: ./manage.py createsuperuser
- Launch the backend: ./manage.py runserver backend

Extras
------

If you would like to launche several environments you may use the port number after the choosen environment, example:
```
./manage.py runserver backend          # It will start backend on port 8000
./manage.py runserver frontend 8001    # It will start frontend on port 8001
```

About the authors
---------------------
**Name:** Juanmi Taboada
**E-Mail:** juanmi@juanmitaboada.com
**GitHub:** https://github.com/juanmitaboada

**Name:** Juan Soler
**E-Mail:** soleronline@gmail.com
**GitHub:** https://github.com/soleronline
