- Create your repo on GitHub
- Set That repo in your local system
- Choose proper location and open that location inside CMD
- Clone that repo inside proper location using CMD

...\(choose-location)> git clone https://github.com/Witzcode0/foodkit.git
...\(choose-location)> cd foodkit
...\(choose-location)\foodkit> 

- Make sure you have installed python in you local system
...\(choose-location)\foodkit> python --version
Python 3.13.3

- Now create virtual env.
...\(choose-location)\foodkit> python -m venv |env-name|

- Activate/Deactivate your env.
Activate:
...\(choose-location)\foodkit> |env-name|\Scripts\activate 
Deactivate:
(|env-name|)...\(choose-location)\foodkit> |env-name|\Scripts\deactivate 

- create requirements.txt in your base dir
(|env-name|)...\(choose-location)\foodkit> type nul > requirements.txt

- Now, install Django
(|env-name|)...\(choose-location)\foodkit> pip install django

- Check install modules and packages:
(|env-name|)...\(choose-location)\foodkit> pip list/pip freeze

- Add installed package inside requirements.txt
(|env-name|)...\(choose-location)\foodkit> pip freeze > requirements.txt

- Install or upgrade module and packages from requirements.txt
(|env-name|)...\(choose-location)\foodkit> pip install -r requirements.txt

- Make sure you have installed django in env.
(|env-name|)...\(choose-location)\foodkit> python
Python 3.13.3 (tags/v3.13.3:6280bb5, Apr  8 2025, 14:47:33) [MSC v.1943 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import django
>>> django.get_version()
'6.0'

OR

(|env-name|)...\(choose-location)\foodkit> python -m django --version
6.0

OR

(|env-name|)...\(choose-location)\foodkit> pip list
Package  Version
-------- -------
asgiref  3.11.0
Django   6.0
pillow   12.0.0
pip      25.3
sqlparse 0.5.5
tzdata   2025.3

- Now, Creating a project
(|env-name|)...\(choose-location)\foodkit> django-admin startproject |project| .

- migrate all table inside the database:
(|env-name|)...\(choose-location)\foodkit> python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK

  Run your django project:
(|env-name|)...\(choose-location)\foodkit> python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 23, 2025 - 16:28:31
Django version 6.0, using settings 'project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

- Create your super user
(|env-name|)...\(choose-location)\foodkit> python manage.py createsuperuser
Username (leave blank to use 'hello'): admin
Email address: admin@gmail.com
Password: ********
Password (again): ********
The password is too similar to the username.
This password is too short. It must contain at least 8 characters.
This password is too common.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.


Now create django apps
(|env-name|)...\(choose-location)\foodkit> mkdir apps
(|env-name|)...\(choose-location)\foodkit> cd apps
(|env-name|)...\(choose-location)\foodkit\apps> mkdir master
(|env-name|)...\(choose-location)\foodkit\apps> mkdir users
(|env-name|)...\(choose-location)\foodkit\apps> mkdir store
(|env-name|)...\(choose-location)\foodkit\apps> cd..
(|env-name|)...\(choose-location)\foodkit> python manage.py startapp |app-name| apps/|app-name|


Go to the |app-name| dir
Now open apps.py file and change path of apps

from django.apps import AppConfig


class StoreConfig(AppConfig):
    name = 'apps.|app-name|' # here add apps.

Now register your app in project/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.master',
    'apps.users',
    'apps.store',
]

create urls,templates, static and media dir or file

apps/store/
  - urls.py  - create urls.py
  - templates - create dir
      - store - create dir
          - index.html
          - about.html
          - products.html ....
  - static - create dir
      - store - create dir

setup static and media dir path in project/settings.py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

go and setup static and media dir url in project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

------------------------------------

git add .
git commit -m "type message here..."
git push
