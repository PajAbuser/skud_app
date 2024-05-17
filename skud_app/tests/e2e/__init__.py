import os
import sys


sys.path.append(os.getcwd())
# print(os.getcwd())

from skud_app import models as sk
# print("blablalb", sk)

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.update({'DJANGO_SETTINGS_MODULE': 'skud.settings'})
# os.environ.update({'PYTHONPATH': 'skud.skud_app'}) 
