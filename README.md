# Great Transformation App

This is the code repo for a Django based web application developed in the context of the project "The Great Transformation. State and Communal Civil Service in Vienna, 1918–1920".


## How To(s) for data curators

### Accounts

Log in to the application's admin interface. Therefore browse to `<baseURL>/admin` like [https://gtrans.acdh.oeaw.ac.at/admin](https://gtrans.acdh.oeaw.ac.at/admin). If you don't have an account yet, ask a responsible person to create one.

#### To create an account

1. log into the 'admin interface' (see above)
2. Under **AUTHENTICATION AND AUTHORIZATION** click on **Users** (or brwose directly to `<baseURL>/admin/auth/user/` [https://gtrans.acdh.oeaw.ac.at/admin/auth/user/](https://gtrans.acdh.oeaw.ac.at/admin/auth/user/))
3. Here click on ** ADD USER** button (top right corner)
4. Provide a username and a passwort.
5. Click **Save and continue editing**
6. Fill out the forms in the next page according to your needs.

#### modify an existing account

In case you want to modify an existing account, e.g. change your username, name, password, ...

1. log in to the admin interface (see above)
2. to change the password click on **CHANGE PASSWORD** (top right corner) and change the password.
3. If you want to change other things like the username, email address, ... you need to be superuser or you have to ask someone who is superuser.  


# Basic info about a django models

The actual data model is described in [this gsheet](https://docs.google.com/spreadsheets/d/1J_TPEl77lCaDPKocJAj0aVPzWcoQbtWDFyBv1BXzbdA/edit?usp=sharing)

## Tables/Classes

* each sheet describes one database table (aka class)
* *field name* is used as internal name, needs to follow specific naming conventions, not visible to anyone who does not read the application's source code.
* *verbose name* provides the visible name.
* *helptext* used to store a (short) explanation/definition of this field/property, can e.g. be displayed as helptext next to a form field.
* *field type* defines the type of the field -> see below.


## fields/properties

* [CharField](https://docs.djangoproject.com/en/2.0/ref/models/fields/#django.db.models.CharField) is used to store *short* texts (strings). In the edit/create interface such a field will be displayed as an input field (usually ony one line long)
* [TextField](https://docs.djangoproject.com/en/2.0/ref/models/fields/#django.db.models.TextField) is used to store texts (strings), no matter how long they are. In the edit/create interface such a field will be displayed as input field covering several lines.
* [FloatField](https://docs.djangoproject.com/en/2.0/ref/models/fields/#floatfield) is used to store a floating point number. Will be displayed as input field accepting numbers only.
* [DateField](https://docs.djangoproject.com/en/2.0/ref/models/fields/#django.db.models.DateField) is used to store a date matching this pattern *YYYY-MM-DD*. In the edit/create interface such a field could be displayed as simple input field or as some kind of calendar, where users can select a date.
* [FK](https://docs.djangoproject.com/en/2.0/ref/models/fields/#foreignkey) stands for a *Foreign Key* relation, meaning that this field stores the primary key of the related class. In the edit/create interface such a field will be displayed as drop-down list or as an autocomplete field
* [M2M](https://docs.djangoproject.com/en/2.0/ref/models/fields/#manytomanyfield) stand for *Many to Many* relation, meaning that this field stores 0:n primary keys of related classe. In the edit/create interface such a field will be displayed as drop-down list with the otpion so select multiple lines or as an autocomplete field, again with the option to select multiple rlated objects.
