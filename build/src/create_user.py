'''
args:
    username
    email
    password
'''
import sys 
import os 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "latrom.settings")
import django 
django.setup()

from django.contrib.auth.models import User
User.objects.create_superuser(sys.argv[1], sys.argv[2], sys.argv[3])