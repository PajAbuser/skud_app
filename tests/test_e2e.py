import json
import os
import sys
import pytest
import random
import math
from uuid import uuid4
from datetime import datetime
from ..skud_app.models import *
from ..skud_app.views import SKUDViewSet, SKUD_Service


class TestE2e:

    def test_pass_creation(self, req):
        SKUDViewSet.skudView.add_pass(req)
        pas = self.skudView.skudServ.skud.passes.get(req.get("Pass").get("id"))
        print(pas.__dict__)
        assert pas.__dict__ == {
            "id": req.get("Pass").id,
            "username": req.get("Pass").username,
            "fio": req.get("Pass").fio,
        }

    def test_door_creation(self, req):
        SKUDViewSet.skudView.add_door(req)
        pas = self.skudView.skudServ.skud.doors.get(req.get("Door").get("id"))
        print(pas.__dict__)
        assert pas.__dict__ == {
            "id": req.get("Door").id,
            "cab": req.get("Door").cab,
            "allowed": req.get("Door").allowed,
        }

    def test_get_application_with_wrong_id():
        service = SKUD_Service()
        with pytest.raises(KeyError):
            service.repr_door(id=int(random.Random()))
