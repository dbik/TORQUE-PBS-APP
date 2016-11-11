from base import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = os.environ.get('TORQUE_PBS_APP_SECRET', '')
SECRET_KEY = 'qty@*mdea+f@o-2k)qs5)&7!y)b59-^ccvf4^o7vubskqblj+m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": 'torque_pbs_app_db',#os.environ.get('MYSQL_TORQUE_PBS_APP_DB_NAME', ''),
        "USER": 'aaa', #os.environ.get('MYSQL_USER', ''),
        "PASSWORD": 'aaa', #os.environ.get('MYSQL_PASSWORD', ''),
        "HOST": "localhost",
        "PORT": 3306,
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_PATH = os.path.join(BASE_DIR, '../static')
STATICFILES_DIRS = (
  STATIC_PATH,
)
