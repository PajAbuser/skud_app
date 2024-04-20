import json
import os
import sys
import pytest
import random
import math
from uuid import uuid4
from datetime import datetime
from models import *
from views import SKUDViewSet, SKUD_Service

class E2ETests:

    req :json = {
      "skud_id": "0",
      "Pass":
        {
            "UUID": "1e9c920e-934d-4259-964c-e67f83742176",
            "username": "user1",
            "fio": "Иванов Иван Иванович"
        },
      "Door": {
        "UUID": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
        "cab": "101",
        "status" : True,
        "allowed":
        {
            "1e9c920e-934d-4259-964c-e67f83742176":
            {
                "UUID": "1e9c920e-934d-4259-964c-e67f83742176",
                "username": "user1",
                "fio": "Лаптев Иван Александрович"
            },
            "8d2938e2-bc10-410e-a72a-96e63f321984": {
                "UUID": "8d2938e2-bc10-410e-a72a-96e63f321984",
                "username": "Paj",
                "fio": "sfa"
            }
        }
      }
    }
    
    def test_pass_creation(req):
        SKUDViewSet.skudView.add_pass(req)
        pas = E2ETests.skudView.skudServ.skud.passes.get(req.get("Pass").get('id'))
        print(pas.__dict__)
        assert pas.__dict__ == { 'id': req.get("Pass").id, 'username': req.get("Pass").username, 'fio': req.get("Pass").fio}

    def test_door_creation(req):
        SKUDViewSet.skudView.add_door(req)
        pas = E2ETests.skudView.skudServ.skud.doors.get(req.get("Door").get('id'))
        print(pas.__dict__)
        assert pas.__dict__ == { 'id': req.get("Door").id, 'cab': req.get("Door").cab, 'allowed': req.get("Door").allowed}


    def test_get_application_with_wrong_id():
     service = SKUD_Service()
     with pytest.raises(KeyError):
        service.repr_door(id=int(random.Random())) 