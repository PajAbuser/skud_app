from django.http import HttpResponse, JsonResponse, FileResponse
from skud_app.models import *
from skud_app.serializers import pasSerializer, doorSerializer

class SKUD_Service():
    
    skud : SKUD = SKUD({},{})
    
    passes_n = []
    doors_n  = []
    
    def log(self):
        self.skud.log()

    def add(self, obj):   #Добавление пропуска или двери в СКУД
        if type(obj) == Door:
            if not self.skud.doors.get(obj.id):
                self.skud.doors.update({obj.id:obj})
                self.doors_n.append(obj.id)
        elif type(obj) == Pas:
            if not self.skud.passes.get(obj.id):
                self.skud.passes.update({obj.id:obj})
                self.passes_n.append(obj.id)
            else: return HttpResponse(content={'message':f"{type(obj)} is already in SKUD"})
        else: return HttpResponse(content={'message':f"for {type(obj)} type there is no storage in SKUD"})

    def reg(self, door1, pas1):   #Зарегистрировать пропуск для открытия двери
        if type(door1) == Door and type(pas1) == Pas:

            if not self.skud.doors.get(door1.id):
                self.skud.doors.update({door1.id:door1})
            elif not door1.allowed.get(pas1.id):
                door1.allowed.update({pas1.id:pas1})

    def rem(self, door1, pas1):   #Удалить регистрацию пропуска
        if type(door1) == Door and type(pas1) == Pas:
            door1.allowed.popitem(pas1)
        elif type(door1) == str and type(pas1) == str:        
            if self.skud.doors.get(door1) == None:
                return HttpResponse(content=f"no such door in SKUD")
            if self.skud.doors.get(door1).allowed.get(pas1) == None:
                if self.skud.passes.get(pas1) == None:
                    return HttpResponse(content=f"no such pass in SKUD")
                else: return HttpResponse(content=f"this pass {self.skud.passes.get(pas1)} is not registered in door {self.skud.doors.get(door1)}")
            else: self.skud.doors.get(door1).allowed.popitem(pas1)
        return HttpResponse(content=f"pass succesfully removed from door")

    def valid(self, door1, pas1) -> bool:   #Проверить, подходит ли пропус
        if type(door1) == Door and type(pas1) == Pas:
            return bool(door1.allowed.get(pas1))
        elif type(door1) == str and type(pas1) == str:
            for door in self.skud.doors:
                if door.id == door1:
                    for pas in self.skud.passes:
                        if pas1 == pas.id:
                            return bool(door.allowed.get(pas.id))
        return False
                    
    def unlock(self, door1):   #Открыть дверь
        if type(door1) == Door:
            door1.status = False
        elif type(door1) == str:
            for door in self.skud.doors:
                if door.id == door1:
                    self.skud.unlock(door)

    def lock(self, door1):   #Закрыть дверь
        if type(door1) == Door:    
            door1.status = True
        elif type(door1) == str:
            for door in self.skud.doors:
                if door.id == door1:
                    self.skud.lock(door)

    def check(self, door1, pas1):   #Поменять состояние двери, если пропуск подходит
        if type(door1) == Door and type(pas1) == Pas:      
            if self.skud.valid(door1, pas1):
                if door1.status:
                    self.skud.unlock(door1)
            else: self.skud.lock(door1)
        elif type(door1) == str and type(pas1) == str:
            if self.skud.valid(door1, pas1):
                for door in self.skud.doors:
                    if door.id == door1:
                        if door.status:
                            self.skud.unlock(door)
                        else: self.skud.lock(door)

    def logs(self):
        f = open("filename.txt")
        for line in self.skud.history:
            f.write(f"{line}\n")
        f.close()
            
    def edit(self, cab, id):
            self.cab = cab
            self.id = id