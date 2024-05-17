import datetime
import inspect
import os
import django.core.serializers.json as json_serializer
import functools
import json
from django.http import HttpResponse, JsonResponse, FileResponse, HttpRequest
from rest_framework import request
from django.views.decorators.csrf import csrf_exempt
from skud_app.models import *
from skud_app.serializers import *
from rest_framework.viewsets import ViewSet
from skud_app.services.SKUD_Service import SKUD_Service
from rest_framework.parsers import JSONParser
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, OpenApiParameter
from rest_framework.decorators import action
from skud_app.services.Running_Service import *
from skud_app.scheduler import scheduler, DateTrigger, CronTrigger
from functools import wraps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import viewsets
       
def log_calls(file_name):
    def decorator(cls):
        for name, func in vars(cls).items():
            if callable(func):
                setattr(cls, name, log_call(file_name)(func))
        return cls
    return decorator

def log_call(file_name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            with open(file_name, 'a') as f:
                f.write(f"<{datetime.datetime.now()}> Invoked method {'{:>16}'.format(func.__name__)} with args {'{:>90}'.format(repr(args[0]))} and keywords {repr(kwargs)}")
                try:
                    f.write(f"through {'localhost' if args[0].META.get('HTTP_X_FORWARDED_FOR') == None else args[0].META.get('HTTP_X_FORWARDED_FOR')} \n")
                except Exception: pass
            res = func(self, *args, **kwargs)
            print(self.skudServ)
            return res
        return wrapper
    return decorator

@extend_schema_view(
add_pass          =extend_schema(summary='Add new pass(es) to SKUD'                 , request=PasDictSerializer  , responses=SKUDSerializer),
repr_pass         =extend_schema(summary='Represent pass in SKUD'                                                , responses=SKUDSerializer),
repr_passes       =extend_schema(summary='Represent all pass in SKUD'                                            , responses=SKUDSerializer),
repr_passes_door  =extend_schema(summary='Returns all registered passes in door'    , request=OperationSerializer, responses=SKUDSerializer),
add_door          =extend_schema(summary='Add new door(s) to SKUD'                  , request=DoorDictSerializer , responses=SKUDSerializer),
repr_door         =extend_schema(summary='Represent door in SKUD'                                                , responses=SKUDSerializer),
repr_doors        =extend_schema(summary='Represent all door in SKUD'                                            , responses=SKUDSerializer),
add_door_pass     =extend_schema(summary='Add pass(es) to door & SKUD if none'      , request=PasDictSerializer  , responses=SKUDSerializer),
remove_passes     =extend_schema(summary='Remove pass(es) from door'                , request=PasDictSerializer  , responses=SKUDSerializer),
remove_pass       =extend_schema(summary='Remove pass from door by their sub-id'    , request=PasDictSerializer  , responses=SKUDSerializer),
export            =extend_schema(summary='Get log by operation id'                  , request=OperationSerializer, responses=SKUDSerializer),
export_logs       =extend_schema(summary='Long-running operation for exporting logs', request=OperationSerializer, responses=SKUDSerializer),
export_logs_infile=extend_schema(summary='Get logs exported in file'                , request=OperationSerializer, responses=SKUDSerializer),
check1            =extend_schema(summary='Checks if pass is registered in door'     , request=OperationSerializer, responses=SKUDSerializer),
check2            =extend_schema(summary='Checks if pass is registered in door'     , request=OperationSerializer, responses=SKUDSerializer),

)
@log_calls("method_calls.log")
class SKUDViewSet(ViewSet):
    serializer_class = SKUDSerializer
    
    skudServ = SKUD_Service()
    opServ = OperationsService()
    
    @action(detail=False)
    def export(self, request, id:str): # -> operation.get(id).result || "Operation is still running"
            id = UUID(id)
            if self.opServ.operations.get(id).done:
                return FileResponse(open(self.opServ.operations.get(id).result, 'rb'))
            else: return HttpResponse(content="Operation is still running")

    @action(detail=False)
    def export_logs(self, request):  # -> operation_id
        operation_id = self.opServ.create_operation()
        scheduler.add_job(self.export_logs_infile, trigger=DateTrigger(datetime.datetime.now()), args=(operation_id, ))
        if not scheduler.running: scheduler.start()
        return HttpResponse(JsonResponse({'operation_id':operation_id}))

    @action(detail=False)
    def export_logs_infile(self, operation_id:UUID):  # -> None
        name = "method_calls.log"
        self.opServ.finish_operation(operation_id, name)

    @action(detail=True, methods=['post'])
    def add_pass(self, request):  # -> skud.export()
        pas = PasDictSerializer(data=request.data)
        print('pas.is_valid() =', pas.is_valid())
        for p in pas.create(): self.skudServ.add(p)
        return Response(data=self.skudServ.skud.export())

    @action(detail=True, methods=['get'], url_path='passes/<int:id>')
    def repr_pass(self, request, id):  # -> str(Pas)
        if len(self.skudServ.passes_n) > id:
            return Response(data=f"{self.skudServ.skud.passes.get(self.skudServ.passes_n[id])}")
        else: 
            return Response(data="No such pass")

    @action(detail=False, methods=['get'], url_path='passes/')
    def repr_passes(self, request):  # -> str(repr_passes_n)
        return Response(data=f"{self.skudServ.repr_passes_n()}")
        
    @action(detail=True, methods=['get'], url_path='doors/<int:id>/passes/') 
    def repr_passes_door(self, request, id):  # -> str(repr_passes_of_door)
        return Response(data=self.skudServ.repr_passes_of_door(id))
        
    @action(detail=True, methods=['post'], url_path='doors/')
    def add_door(self, request):  # -> skud.export()
        door = DoorDictSerializer(data=request.data)
        print('door.is_valid() =',door.is_valid())
        if (type(door.create()) == list): 
            for d in door.create(): self.skudServ.add(d)
        else: self.skudServ.add(door.create())
        return Response(data=self.skudServ.skud.export())
    
    @action(detail=True, methods=['get'], url_path='doors/<int:id>')
    def repr_door(self, request, id):  # -> str(Door)
        if len(self.skudServ.doors_n) > id:
            return Response(data=f"{self.skudServ.skud.doors.get(self.skudServ.doors_n[id])}")
        else:
            return Response(data="No such door")

    @action(detail=False, methods=['get'], url_path='doors/')
    def repr_doors(self, request):  # -> str(repr_doors_n)
        return Response(data=f"{self.skudServ.repr_doors_n()}")

    @action(detail=True, methods=['post'], url_path='doors/<int:id>/passes')
    def add_door_pass(self, request, id):  # -> "pass(es) [Pas] is added to door Door"
        pas = PasDictSerializer(data=request.data)
        pas.is_valid()
        door = self.skudServ.skud.doors.get(self.skudServ.doors_n[id])
        sp = "pass"
        if type(pas.create()) == list:
            for p in pas.create():
                self.skudServ.reg(door,p)
                sp += ("es " if sp == "pass" else ", ") + str(p.id)
        else: self.skudServ.reg(door,pas.create())
        return Response(data=f"pass {pas.create()} is added to door {door.id}")

    @action(detail=True, methods=['delete'], url_path='doors/<int:id>/passes')
    def remove_passes(self, request):  # -> repr_door + skud.export()
        data = request.data
        door = self.skudServ.skud.doors.get(data.get('door').get('id'))
        for pas in data.get("Passes"):
            self.skudServ.rem(door, pas)
        self.repr_door(door)
        return Response(data=self.skudServ.skud.export())

    @action(detail=True, methods=['delete'], url_path='doors/<int:door_id>/passes/<int:pass_id>')
    def remove_pass(self, request, door_id: int, pass_id: int):  # -> skud.export()
        self.skudServ.skud.doors.get(self.skudServ.doors_n[door_id]).allowed.pop(self.skudServ.passes_n[pass_id])
        return Response(data=self.skudServ.skud.export())

    @action(detail=True, methods=['post'], url_path='check/')
    def check1(self, request):  # -> check(door, pas)
        data = request.data
        door1 = self.skudServ.skud.doors.get(data.get('doors').get('id'))
        if door1 == None:
            self.add_door(request)
            door1 = self.skudServ.skud.doors.get(data.get('doors').get('id'))
        pass1 = self.skudServ.skud.passes.get(data.get('passes').get('id'))
        if pass1 == None:
            self.add_pass(request)
            pass1 = self.skudServ.skud.passes.get(data.get('passes').get('id'))
        return Response(data=f"{self.skudServ.check(door1,pass1)}")

    @action(detail=True, methods=['get'], url_path='check/<int:door_id>/<int:pass_id>')
    def check2(self, request, door_id:int, pass_id:int):  # -> "pass Pas is valid to door Door"
        door1 = self.skudServ.doors_n[door_id]
        pass1 = self.skudServ.passes_n[pass_id]
        self.skudServ.check(door1,pass1)
        return Response(data=f"pass {pass1} is valid to door {door1}")    
        

@extend_schema_view(
    getOperation=extend_schema(summary='Get information about operation', request=OperationSerializer, responses=OperationSerializer)
)
class OperationViewSet(ViewSet):
    
    OpServ = OperationsService()
        
    @action(detail=True, methods=['get'])
    def getOperation(self, id):
        return self.OpServ.get_operation(id)