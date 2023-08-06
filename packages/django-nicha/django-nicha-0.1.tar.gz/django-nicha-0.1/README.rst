========
Nicha
========

Nicha is a django package that automates the process of creating the commune web pages,
as well as the main features in any django web application.
Named after mythological girl that knows all the answers and holds the keys to finding purpose on life.


Quick Start:
------------

1. Add Nicha to your INSTALLED_APPS setting like this::
		
		INSTALLED_APPS = [
			...
			'nicha',
		]

2. Include the nicha URLconf in your project urls.py like this::
		path('nicha/', include('nicha.urls')),

3. Run `python3 manage.py migrate` to create the nicha models.


 