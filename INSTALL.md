Installation instructions
=========================

To install mail:
https://github.com/SmileyChris/django-mailer-2/blob/master/docs/usage.txt#L63

This server is intended to be installed using virtualenv. For installing python packages in the virtual environment, a requirements.txt files is provided.
Install pip, virtualenv and virtualenvwrapper. In Ubuntu:
	sudo apt-get install python-pip virtualenv virtualenvwrapper
After installation, create a new virtualenv using mkvirtualenv.
Enable virtualenv running:
	workon <virtual env>
Once inside virtualenv, install packages using pip:
	pip install -r requirements.txt

To configure the database, copy the settings_local_example.py file to settings_local.py and configure it properly setting the database engine and parameters.
