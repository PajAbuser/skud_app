from django.db import models
from uuid import UUID


class Pas:

    id:       UUID
    username: str
    fio:      str

    def __init__(self, *params, json=None) -> None:
        if json != None:
            self.username = json.get("username")
            self.fio = json.get("fio")
            self.id = json.get("UUID")
            return None
        if type(params) == tuple:
            params        = dict(params[0])
            self.username = params.get("username")
            self.fio      = params.get("fio")
            self.id       = params.get("UUID")

    def __repr__(self) -> str:
        return (
            "pas object = {"
            + f"id: {str(self.id)}, username: {self.username}, fio: {self.fio}"
            + "}"
        )


class Door:

    id:      UUID
    cab:     str
    allowed: dict[UUID, Pas]
    status:  bool  # False - open, True - closed

    def __init__(self, *params, json=None) -> None:
        self.allowed = {"0": None}
        self.allowed.popitem()
        if json != None:
            self.cab     = json.get("cab")
            self.id      = json.get("UUID")
            self.allowed = json.get("passes")
            return None
        if type(params) == tuple:
            params   = dict(params[0])
            self.cab = params.get("cab")
            self.id  = params.get("id")
            if params.get("passes") != []: 
                for p in (params.get("passes")): self.allowed[p.id] = p 
            else: self.allowed = []
            self.status = params.get("status")

    def __repr__(self) -> str:
        return (
            "door object = {"+f"id: {self.id}, cab: {self.cab}, status: {self.status},\n" +
            "    allowed_passes: {" + f'\n' + ",\n".join(f"        {key}: {value}" for key, value in self.allowed.items()) + f'\n' + "    }"
        )


class SKUD:

    passes: dict[str, Pas]  = {}
    doors:  dict[str, Door] = {}

    def __init__(self, doors: dict[str, Door], passes: dict[str, Pas], *args, **kwargs):
        self.doors = doors
        self.allowed = passes
        self.history = open("method_calls.log", "a")

    def __repr__(self) -> str:
        return  "\nSKUD passes: {" + f'\n' + ",\n".join(f"    {key}: {value}" for key, value in self.passes.items()) + f'\n' + "}\n" + \
                 "\nSKUD doors: {" + f'\n' + ",\n".join(f"    {key}: {value}" for key, value in self.doors .items()) + "\n}\n"


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
