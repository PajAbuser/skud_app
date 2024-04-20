import os
import sys
import pytest
import random
import math
from uuid import uuid4
from datetime import datetime
from models import *
# from services.SKUD_Service import *

class UnitTest:

    def randomString(length:int) -> str:
        # for (i = 0, i < length, i++):
        string = ""
        for i in length:
            string += chr(int(random.Random())%65)
        return string

    def randomPas(length:int) -> Pas:
        passes: dict[str,Pas] = {}
        for i in length:
            id:       UUID = uuid4()
            username: str  = UnitTest.randomString(10)
            fio:      str  = UnitTest.randomString(20)
            passes.update[id] = Pas(id,username,fio)
        return passes

    def test_pass_creation():
        id:       UUID = uuid4()
        username: str  = UnitTest.randomString(10)
        fio:      str  = UnitTest.randomString(20)
        pas            = Pas(id,username,fio)
        print(pas.__dict__)
        assert pas.__dict__ == { 'id': pas.id, 'username': pas.username, 'fio': pas.fio}

    def test_door_creation():
        id:      UUID            = uuid4()
        cab:     str             = UnitTest.randomString(10)
        allowed: dict[str, Pas]  = UnitTest.randomPas(10)
        door = Door(id,cab,allowed)
        print(door.__dict__)
        assert door.__dict__ == { 'id': door.id, 'cab': door.cab, 'allowed': door.allowed}

    # def test_get_application_with_wrong_id():
    #  service = SKUD_Service()
    #  with pytest.raises(KeyError):
    #     service.repr_door(id=int(random.Random())) 