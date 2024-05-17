import json
import os
import sys
import pytest
import random
import math
from uuid import uuid4
from datetime import datetime
from skud_app.models import *
from skud_app.views import SKUDViewSet, SKUD_Service
from rest_framework.request import Request
from django.http import HttpRequest
import requests


base_url = f'http://127.0.0.1:8000'

class TestE2e:
    
    '''
        resp = requests.post(f'{base_url}/applications/', json={
            'user_id': uid.hex,
            'start': start,
            'finish': finish
        }).json()

        assert resp['status'] == 'CREATED'
        assert resp['start'] == start
        assert resp['finish'] == finish
        assert resp['driver_id'] == None
        assert (datetime.now() - datetime.strptime(resp['created_date'].split('.')[0], '%Y-%m-%dT%X')).total_seconds() < 2
    '''
    
    def test_pass_creation(self):
        id = str(uuid4())
        resp = requests.post(f'{base_url}/passes/', json=
        {
            "passes"  : [
                {
                    "id"      :  str(id),
                    "username": f"username_{id}",
                    "fio"     : f"fio_{id}"
                }
            ]
        }
        ).json()
        
        found = False
        for p in resp['passes']:
            if ((p['id'      ] == str(id)) and
                (p["username"] == f"username_{id}") and
                (p["fio"     ] == f"fio_{id}")):
                found = True
        assert found
    
    def test_passes_creation(self):
        id1 = str(uuid4())
        id2 = str(uuid4())
        resp = requests.post(f'{base_url}/passes/', json=
        {
            "passes"  : [
                {
                    "id"      :  str(id1),
                    "username": f"username_{id1}",
                    "fio"     : f"fio_{id1}"
                },
                {
                    "id"      :  str(id2),
                    "username": f"username_{id2}",
                    "fio"     : f"fio_{id2}"
                }
            ]
        }
        ).json()
        found1 = False
        found2 = False
        for p in resp['passes']:
            if ((p['id'      ] == str(id1)) and
                (p["username"] == f"username_{id1}") and
                (p["fio"     ] == f"fio_{id1}")):
                found1 = True
            if ((p['id'      ] == str(id2)) and
                (p["username"] == f"username_{id2}") and
                (p["fio"     ] == f"fio_{id2}")):
                found2 = True
        assert found1 and found2

    def test_door_creation(self):
        idp = str(uuid4())
        idd = str(uuid4())
        resp = requests.post(f'{base_url}/doors/', json=
        {
            "doors": [
                {
                "passes": [
                    {
                    "id"      :  str(idp),
                    "username": f"username_{idp}",
                    "fio"     : f"fio_{idp}"
                    }
                ],
                "id"    : str(idd),
                "cab"   : f"cab_{idd}",
                "status": True
                }
            ]
        }
        ).json()
        found_p_in_p = False
        found_d_in_d = False
        found_p_in_d = False
        for p in resp['passes']:
            if ((p['id'      ] == str(idp)) and
                (p["username"] == f"username_{idp}") and
                (p["fio"     ] == f"fio_{idp}")):
                found_p_in_p = True
        for d in resp['doors']:
            if ((d['id' ] ==    str(idd) ) and
                (d["cab"] == f"cab_{idd}")):
                found_d_in_d = True
                for pp in d['passes']:
                    if ((pp['id'      ] == str(idp)) and
                        (pp["username"] == f"username_{idp}") and
                        (pp["fio"     ] == f"fio_{idp}")):
                        found_p_in_d = True
        assert found_p_in_d and found_d_in_d and found_p_in_p

    def test_pass_creation(self):
        id = str(uuid4())
        resp = requests.post(f'{base_url}/passes/', json=
        {
            "passes"  : [
                {
                    "id"      :  str(id),
                    "username": f"username_{id}",
                    "fio"     : f"fio_{id}"
                }
            ]
        }
        ).json()
        
        found = False
        for p in resp['passes']:
            if ((p['id'      ] == str(id)) and
                (p["username"] == f"username_{id}") and
                (p["fio"     ] == f"fio_{id}")):
                found = True
        assert found
    
    def test_a(self):
        id = str(uuid4())
        resp = requests.post(f'{base_url}/passes/', json=
        {
            "passes"  : [
                {
                    "id"      :  str(id),
                    "username": f"username_{id}",
                    "fio"     : f"fio_{id}"
                }
            ]
        }
        ).json()
        
        found = False
        for p in resp['passes']:
            if ((p['id'      ] == str(id)) and
                (p["username"] == f"username_{id}") and
                (p["fio"     ] == f"fio_{id}")):
                found = True
        assert found

    def test_b(self):
        id = str(uuid4())
        resp = requests.post(f'{base_url}/passes/', json=
        {
            "passes"  : [
                {
                    "id"      :  str(id),
                    "username": f"username_{id}",
                    "fio"     : f"fio_{id}"
                }
            ]
        }
        ).json()
        
        found = False
        for p in resp['passes']:
            if ((p['id'      ] == str(id)) and
                (p["username"] == f"username_{id}") and
                (p["fio"     ] == f"fio_{id}")):
                found = True
        assert found

    def test_c(self):
        id = str(uuid4())
        resp = requests.post(f'{base_url}/passes/', json=
        {
            "passes"  : [
                {
                    "id"      :  str(id),
                    "username": f"username_{id}",
                    "fio"     : f"fio_{id}"
                }
            ]
        }
        ).json()
        
        found = False
        for p in resp['passes']:
            if ((p['id'      ] == str(id)) and
                (p["username"] == f"username_{id}") and
                (p["fio"     ] == f"fio_{id}")):
                found = True
        assert found
