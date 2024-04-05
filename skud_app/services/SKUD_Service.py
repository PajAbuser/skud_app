from django.http import HttpResponse, JsonResponse, FileResponse
from skud_app.models import *


class SKUD_Service():
    
    skuds : dict[str, SKUD] = {}
    
    def __init__(self):
        self.skuds.update({'0':SKUD({},{})})   
            
    def create(self) -> int:
        self.skuds.update({str(len(self.skuds)):SKUD({},{})})
        return HttpResponse(content={'id: 'f'{len(self.skuds)-1}'})

    def log(self, id = '0'):
        self.skuds.get(id).log()

    def add(self, obj, id = '0'):   #Добавление пропуска или двери в СКУД
        if type(obj) == Door:
            if not self.skuds.get(id).doors.get(obj.id):
                self.skuds.get(id).doors.update({obj.id:obj})
        elif type(obj) == Pas:
            if not self.skuds.get(id).passes.get(obj.id):
                self.skuds.get(id).passes.update({obj.id:obj})
            else: return HttpResponse(content={'message':f"{type(obj)} is already in (custom)"})
        else: return HttpResponse(content={'message':f"for {type(obj)} type there is no storage (custom) "})

    def reg(self, door1, pas1, id = '0'):   #Зарегистрировать пропуск для открытия двери
        if type(door1) == Door and type(pas1) == Pas:

            if not self.skuds.get(id).doors.get(door1.id):
                self.skuds.get(id).doors.update({door1.id:door1})
            elif not door1.allowed.get(pas1.id):
                door1.allowed.update({pas1.id:pas1})

    def rem(self, door1, pas1, id = '0'):   #Удалить регистрацию пропуска
        if type(door1) == Door and type(pas1) == Pas:
            door1.allowed.remove(pas1)
        elif type(door1) == str and type(pas1) == str:        
            for door in self.skuds.get(id).doors:
                if door.id == door1:
                    for pas in self.skuds.get(id).passes:
                        if pas1 == pas.id:
                            if door.allowed.get(pas.id):
                                door.allowed.remove(pas)

    def valid(self, door1, pas1, id = '0') -> bool:   #Проверить, подходит ли пропус
        if type(door1) == Door and type(pas1) == Pas:
            return bool(door1.allowed.get(pas1))
        elif type(door1) == str and type(pas1) == str:
            for door in self.skuds.get(id).doors:
                if door.id == door1:
                    for pas in self.skuds.get(id).passes:
                        if pas1 == pas.id:
                            return bool(door.allowed.get(pas.id))
        return False
                    
    def unlock(self, door1, id = '0'):   #Открыть дверь
        if type(door1) == Door:
            door1.status = False
        elif type(door1) == str:
            for door in self.skuds.get(id).doors:
                if door.id == door1:
                    self.skuds.get(id).unlock(door)

    def lock(self, door1, id = '0'):   #Закрыть дверь
        if type(door1) == Door:    
            door1.status = True
        elif type(door1) == str:
            for door in self.skuds.get(id).doors:
                if door.id == door1:
                    self.skuds.get(id).lock(door)

    def check(self, door1, pas1, id = '0'):   #Поменять состояние двери, если пропуск подходит
        if type(door1) == Door and type(pas1) == Pas:      
            if self.skuds.get(id).valid(door1, pas1):
                if door1.status:
                    self.skuds.get(id).unlock(door1)
            else: self.skuds.get(id).lock(door1)
        elif type(door1) == str and type(pas1) == str:
            if self.skuds.get(id).valid(door1, pas1):
                for door in self.skuds.get(id).doors:
                    if door.id == door1:
                        if door.status:
                            self.skuds.get(id).unlock(door)
                        else: self.skuds.get(id).lock(door)

    def logs(self, id = '0'):
        f = open("filename.txt")
        for line in self.skuds.get(id).history:
            f.write(f"{line}\n")
        f.close()
            
    def edit(self, cab, id):
            self.cab = cab
            self.id = id