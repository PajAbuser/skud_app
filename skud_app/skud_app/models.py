import json
from django.db import models
from uuid import UUID


class Pas:

    id:       UUID
    username: str
    fio:      str

    def __init__(self, *params, json=None) -> None:
        if type(params) == tuple:
            params        = dict(params[0])
            self.username = params.get("username")
            self.fio      = params.get("fio")
            self.id       = str(params.get("id"))

    def __repr__(self) -> str:
        return (
            "pas object = {"
            + f"id: {self.id}, username: {self.username}, fio: {self.fio}"
            + "}"
        )
        
    def to_dict(self):
        return {
            'id': str(self.id),
            'username': self.username,
            'fio': self.fio
        }

class Door:

    id:      UUID
    cab:     str
    passes: dict[UUID, Pas]
    status:  bool  # False - open, True - closed

    def __init__(self, *params, json=None) -> None:
        self.passes = {"0": None}
        self.passes.popitem()
        if type(params) == tuple:
            params   = dict(params[0])
            self.cab = params.get("cab")
            self.id  = str(params.get("id"))
            if params.get("passes") != []: 
                for p in (params.get("passes")): self.passes[p.id] = p 
            else: self.passes = []
            self.status = params.get("status")

    def __repr__(self) -> str:
        return (
            "door object = {"+f"id: {self.id}, cab: {self.cab}, status: {self.status},\n" +
            "    allowed_passes: {" + f'\n' + ",\n".join(f"        {key}: {value}" for key, value in self.passes.items()) + f'\n' + "    }"
        )
        
    def to_dict(self):
        return {
            'id': str(self.id),
            'cab': self.cab,
            'passes': [p.to_dict() for p in self.passes.values()],
            'status': self.status
        }
        


class SKUD:

    passes: dict[str, Pas]  = {}
    doors:  dict[str, Door] = {}

    def __init__(self, doors: dict[str, Door], passes: dict[str, Pas], *args, **kwargs):
        self.doors = doors
        self.passes = passes
        self.history = open("method_calls.log", "a")

    def __repr__(self) -> str:
        return "\nSKUD_passes: {" + f'\n' + ",\n".join(f"    {key}: {value}" for key, value in self.passes.items()) + f'\n' + "}\n" + \
                 "\nSKUD_doors: {" + f'\n' + ",\n".join(f"    {key}: {value}" for key, value in self.doors .items()) + "\n}\n"
                 
    def export(self):
        listp = [p.to_dict() for p in self.passes.values()]
        listd = [d.to_dict() for d in self.doors.values()]
        return {
            'passes': listp,
            'doors': listd
        }

class Operation:

    id:     UUID
    done:   bool
    result: any

    def __init__(self, id: UUID, done: bool = False, result=None) -> None:
        self.id = id
        self.done = done
        self.result = result

    def __repr__(self) -> str:
        return "{" + f"id={self.id}, done={self.done}, result={self.result}" + "}"
