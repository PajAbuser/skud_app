import os
import sys
import pytest
import random
import math
from uuid import uuid4
from datetime import datetime
from skud_app.models import *
from skud_app.serializers import *


class TestUnit():
    
    @staticmethod
    def randomString(length: int) -> str:
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return "".join(random.choice(chars) for _ in range(length))

    @staticmethod
    def randomPas(length: int) -> list[Pas]:
        passes = []
        for i in range(length):
            id = str(uuid4())
            username = TestUnit.randomString(10)
            fio = TestUnit.randomString(20)
            pas = Pas({'id':id, 'username':username, 'fio':fio})
            passes.append(pas)
        return passes
        
    def test_pass_creation(self):
        id = str(uuid4())
        username = self.randomString(10)
        fio = self.randomString(20)
        pasSer = PasSerializer(data={'id': id, 'username': username, 'fio': fio})
        pasSer.is_valid()
        pas = pasSer.create()
        assert pas.id == id
        assert pas.username == username
        assert pas.fio == fio

    # def test_door_creation(self):
    #     id = str(uuid4())
    #     cab = self.randomString(10)
    #     passes = self.randomPas(10)
    #     doorSer = DoorSerializer(data={'id': id, 'cab': cab, 'passes': passes, 'tatus': True})
    #     doorSer.is_valid()
    #     door = doorSer.create()
    #     assert door.id == id
    #     assert door.cab == cab
    #     assert door.passes == passes