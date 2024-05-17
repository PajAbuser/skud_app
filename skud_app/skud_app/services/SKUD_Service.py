import datetime
from django.http import HttpResponse
from skud_app.models import *


class SKUD_Service:

    skud: SKUD = SKUD({}, {})

    passes_n: Pas  = []
    doors_n : Door = []
    
    def repr_passes_n(self):
        if not self.passes_n: return 'No passes is SKUD yet\n'
        s = '\npasses sub-id:\n'
        for i in range(len(self.passes_n)):
            s += f"{i}: {self.passes_n[i]} "
        return s
    
    def repr_doors_n(self):
        if not self.doors_n: return 'No doors is SKUD yet\n'
        s = '\n doors sub-id:\n'
        for i in range(len(self.doors_n )):
            s += f"{i}: {self.doors_n [i]} "
        return s
    
    def __repr__(self):
        s = str(self.skud) + self.repr_passes_n() + self.repr_doors_n()
        return s

    def add(self, obj):  # Добавление пропуска или двери в СКУД
        # print('entered add:\n', obj)
        if type(obj) == Door:
            if not self.skud.doors.get(obj.id):
                self.skud.doors.update({obj.id: obj})
                self.doors_n.append(obj.id)
            for pas in obj.passes.values():
                if not self.skud.passes.get(pas.id):
                    self.skud.passes.update({pas.id: pas})
                    self.passes_n.append(pas.id)
        elif type(obj) == Pas:
            if not self.skud.passes.get(obj.id):
                self.skud.passes.update({obj.id: obj})
                self.passes_n.append(obj.id)

    def reg(self, door1, pas1):  # Зарегистрировать пропуск для открытия двери
        self.add(door1)
        self.add(pas1)
        if type(door1) == Door and type(pas1) == Pas:
                door1.passes.update({pas1.id: pas1})

    def rem(self, door1, pas1):  # Удалить регистрацию пропуска
        if type(door1) == Door and type(pas1) == Pas:
            door1.passes.popitem(pas1)
        elif type(door1) == str and type(pas1) == str:
            if self.skud.doors.get(door1) == None:
                return HttpResponse(content=f"no such door in SKUD")
            if self.skud.doors.get(door1).passes.get(pas1) == None:
                if self.skud.passes.get(pas1) == None:
                    return HttpResponse(content=f"no such pass in SKUD")
                else:
                    return HttpResponse(
                        content=f"this pass {self.skud.passes.get(pas1)} is not registered in door {self.skud.doors.get(door1)}"
                    )
            else:
                self.skud.doors.get(door1).passes.popitem(pas1)
        return HttpResponse(content=f"pass succesfully removed from door")

    def valid(self, door1, pas1) -> bool:  # Проверить, подходит ли пропус
        if type(door1) == Door and type(pas1) == Pas:
            return bool(door1.passes.get(pas1))
        elif type(door1) == str and type(pas1) == str:
            return self.skud.doors.get(door1).passes.get(pas1.id)

    def unlock(self, door1):  # Открыть дверь
        if type(door1) == Door:
            door1.status = False
        elif type(door1) == str:
            self.skud.doors.get(door1).status = False

    def lock(self, door1):  # Закрыть дверь
        if type(door1) == Door:
            door1.status = False
        elif type(door1) == str:
            self.skud.doors.get(door1).status = False

    def check(self, door1, pas1):  # Поменять состояние двери, если пропуск подходит
        with open(f"SKUD_{datetime.date}", "a+") as f:
            f.write(
                f"{datetime.datetime.now()} pass:{pas1} is tried to get access to the door:{door1}"
            )
        if type(door1) == Door and type(pas1) == Pas:
            if self.valid(door1, pas1):
                if door1.status:
                    self.unlock(door1)
                else:
                    self.lock(door1)
                return HttpResponse(content=f"pass {pas1} is valid to door {door1}")
            else:
                return HttpResponse(content="Invalid pass")
        elif type(door1) == str and type(pas1) == str:
            door1 = self.skud.doors.get(door1)
            pas1 = self.skud.passes.get(pas1)
            if self.valid(door1, pas1):
                if door1.status:
                    self.unlock(door1)
                else:
                    self.lock(door1)
                return HttpResponse(content=f"pass {pas1} is valid to door {door1}")
            else:
                return HttpResponse(content="Invalid pass")

    def repr_passes_of_door(self, id):
        s = "\n"
        door = self.skud.doors.get(self.doors_n[id])
        for pas in list(door.passes.values()):
            for i in range(len(self.passes_n)):
                if pas.id == self.passes_n[i]:
                    s += f"{i}: {str(pas)}"
        return s
    
    def edit(self, cab, id):
        self.cab = cab
        self.id = id
