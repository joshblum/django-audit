django-audit 
============

### 6.858 Final Project


What is django-audit?
----------------------------
The django-audit is a set of test applications showing proof of concept and a profiling suite for the django-audit-log library.

The `django-forum` code is used as a test application for verify that audit-logs are generated. 

The `ip_loc` application is an example application that monitors if users are accessing the site from different countries or using public TOR exit nodes.

The profiling suite shows usage statistics between running unmodified django and django with auditing enabled. 


Getting Started
----------------------------
Get started cloning the repo:

    git clone git@github.com:joshblum/django-audit.git

And then running:

    sh setup.sh

This will setup a virtual environment and install the required packages. To manually install the required packages run:
    
    pip install -r requirements.txt

This will install a modified version of django whose source can be found here [https://github.com/joshblum/django-with-audit.git](https://github.com/joshblum/django-with-audit.git)

Some basic (single forum, thread, and post) can be imported by running:

    python manage.py loaddata test_data.json

To get the server running run the following command.

    python manage.py runserver

Testing
----------------------------
Tests are provided in both the `forum` app and `ip_loc` app. The tests can be run by the following:
    
    python manage.py test <app_name>

For the `forum` app the tests verify that `audit_log` objects are created.

The `ip_loc` tests verify the correctness of alerting admin when users have suspicious activity patterns.