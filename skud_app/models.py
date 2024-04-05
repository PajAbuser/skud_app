from django.db import models
from uuid import UUID

class Pas:
    
    id:       UUID
    username: str
    fio:      str
    
    def __init__(self, *params, json = None) -> None:
        if json != None:
            self.username = json.get('username')
            self.fio      = json.get('fio')
            self.id       = json.get('UUID')
            return None
        if type(params) == tuple:
            params = dict(params[0])
            self.username = params.get('username')
            self.fio      = params.get('fio')
            self.id       = params.get('UUID')

    def __repr__(self) -> str:
        return "{" + f"id: {str(self.id)}, username: {self.username}, fio: {self.fio}" + "}"

class Door:
    
    id:       UUID
    cab:      str
    allowed:  dict[str, Pas]
    status:   bool #False - open, True - closed
    
    def __init__(self, *params, json = None) -> None:
        self.allowed = {'0':None}
        self.allowed.popitem()
        if json != None:
            self.cab     = json.get('cab')
            self.id      = json.get('UUID')
            self.allowed = json.get('allowed')
            return None
        if type(params) == tuple:
            params = dict(params[0])
            self.cab     = params.get('cab')
            self.id      = params.get('UUID')
            if (params.get('allowed') != {}):
                for p in dict(params.get('allowed')).values():
                    self.allowed.update({p.get('UUID'):p})
            else: self.allowed = {}
            self.status  = params.get('status')

    def __repr__(self) -> str:
            return "\n{" f"id: " + '{:>4}'.format(str(self.id)) + \
                ", cab: " + '{:>7}'.format(self.cab) + \
                    ", status: " + \
                        '{:>1}'.format(str(self.status)) + \
                            ", allowed passes: \n" + '{:>30}'.format(str(self.allowed)) + "}"




class SKUD:

    history: dict[str, object] = {}
    passes:  dict[str, Pas] = {}
    doors:   dict[str, Door] = {}
    
    def __init__(self, doors: dict[str, Door], passes: dict[str, Pas]):
            self.doors = doors
            self.passes = passes

    def __repr__(self) -> str:
        return f"passes: {self.passes}, doors: {self.doors}"