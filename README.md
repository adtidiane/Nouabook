Nouabook
================================

Nouabook is a fork of Votainteligente the electoral platform that Fundación Ciudadano Inteligente uses to transparent the electoral positions of different candidates to an election.
So we reuse the explanation from Votainteligente in ciudadanointeligente/votainteligente-portal-electoral Github


#Installation

Nouabook depends on 3 parts candideit.org, popit and write-it. You might choose to use all of them or just part. In the following document it is described how to install.

## Assumptions

This guide was made using an ubuntu.(you can work with windows but it's better to use a linux system)

## Requirements

Before the installation process is started a number of requirements is needed

- [virtualenv](https://pypi.python.org/pypi/virtualenv)
- [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/)
- [Git](http://git-scm.com/)
- The requirements that [sorl-thumbnail has](http://sorl-thumbnail.readthedocs.org/en/latest/requirements.html)

## Installation process

* Clone votainteligente somewhere in your system.

`git clone https://github.com/adtidiane/Nouabook.git`

Enter the installation directory

`cd Nouabook`

* Create a virtual environment

`mkvirtualenv nouabook_env`

* Install the requirements that votainteligente needs in the current virtualenvironment

`pip install -r requirements.txt`

It might take some time to get all installed

NB: if installation of requirements are not successfull you need to install them one by one.

`example: pip install django-taggit`

* Create the database and tables.

`python manage.py syncdb`

Update the DB with migrations

`python manage.py migrate`

create the migrations for elections app

`python manage.py schemamigration elections --initial`

Update the DB with migrations for elections app

`python manage.py migrate elections`

* Update Database concerning flatpages_i18n

You need to update the DB follow the instruction [here](https://github.com/PragmaticMates/django-flatpages-i18n#installation) at point 6.

## Bringing elections from candideit.org

Elections in VotaInteligente have a one-to-one relation with elections in candideit.org, so for your installation you'll first need to create an election in [candideit.org](http://candideit.org) and follow the next steps.

Specifically for this installation we are not using popit.

* Create the file votainteligente/local_settings.py with the following content.

```
USE_POPIT = False

CANDIDEITORG_URL = http://candideit.org/api/v2/'

CANDIDEITORG_USERNAME = 'YOUR-CANDIDEITORG-USERNAME'

CANDIDEITORG_API_KEY = 'YOUR-CANDIDEITORG-APIKEY'

```

* Getting your elections from candideit.org into your installation.

You need to run the following command

`python manage.py update_from_candidator`

* Running Nouabook

`python manage.py runserver`

And hit http://localhost:8000/.

## Theming

### Created theme

The theme used is for [nouabook](http://nouabook.ma). you can use it and modify it.

### Creating your own custom theme or use the existing theme

If you want to create a new theme you have to create a directory containing two different subdirectories templates and static, and copy the templates that you want to replace.

to use existing theme or new theme in your project, in your settings.py or local_settings.py file you have to add the following

```
 STATICFILES_DIRS = (
     '/full/path/to/your/theme/static/',
 )
 TEMPLATE_DIRS = (
     '/full/path/to/your/theme/templates/',
 )
```

## Facebook publication

you need to create and set up a new facebook app in [developers part](https://developers.facebook.com) make it public, add the `publish_actions` permission
to your app by sending request to be approved by facebook review team to allow everyone to use the permission.

If you don't get yet the permission the listed facebook profils in roles part of app (admin, developer, user test...) are able to use it and send messages.
see More explanation in facebook developer part about review status.


## Licensing

Nouabook.ma of SimSim-Citizen Participation is available under the terms of the [Creative Commons Attribution 4.0 License International]( http://creativecommons.org/licenses/by/4.0/).

Nouabook is based on VotaInteligente which is free and released as open source software covered by the terms of the [GNU Public License](http://www.gnu.org/licenses/gpl-3.0.html) (GPL v3)

