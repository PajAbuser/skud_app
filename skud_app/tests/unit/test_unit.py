import os
import sys
import pytest
import random
import math
from uuid import uuid4
from datetime import datetime
from skud_app.models import *
from skud_app.serializers import *
# from services.SKUD_Service import *


class TestUnit:
    
    @staticmethod
    def randomString(length:int) -> str:
        # for (i = 0, i < length, i++):
        string = ""
        for i in range(length):
            string += chr(int(random.randrange(1,65)))
        return string
    
    @staticmethod
    def randomPas(length:int) -> Pas:
        passes: dict[str,Pas] = {}
        for i in range(length):
            id:       str = str(uuid4())
            username: str = TestUnit.randomString(10)
            fio:      str = TestUnit.randomString(20)
            pasSer = PasSerializer(data={'id':id,'username':username,'fio':fio})
            pasSer.is_valid()
            passes.update({id:pasSer.create()})
        return passes

    def test_fake(self):
        assert 1 == 1
        
    def test_pass_creation(self):
        id:       str = str(uuid4())
        username: str = self.randomString(10)
        fio:      str = self.randomString(20)
        pasSer = PasSerializer(data={'id':id,'username':username,'fio':fio})
        pasSer.is_valid()
        pas = pasSer.create()
        assert pas.__dict__ == { 'id': pas.id, 'username': pas.username, 'fio': pas.fio}

    # def test_door_creation(self):
    #     id:     str            = str(uuid4())
    #     cab:    str            = self.randomString(10)
    #     passes: dict[str, Pas] = self.randomPas(10)
    #     doorSer = DoorSerializer(data={'id':id,'cab':cab,'passes':passes, 'status':True})
    #     doorSer.is_valid()
    #     door = doorSer.create()
    #     print(door.__dict__)
    #     assert door.__dict__ == { 'id': door.id, 'cab': door.cab, 'passes': door.passes}

    
