import datetime
import io
from django.http import HttpResponse, JsonResponse, FileResponse, HttpRequest
import json
from rest_framework import request
from django.views.decorators.csrf import csrf_exempt
from skud_app.models import *
from skud_app.serializers import *
from rest_framework.viewsets import ViewSet
from skud_app.services.SKUD_Service import SKUD_Service
from rest_framework.parsers import JSONParser
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
import django.core.serializers.json as json_serializer
import functools
from skud_app.services.Running_Service import *
from skud_app.scheduler import scheduler, DateTrigger


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        req  = args[1]
        with open('method_calls.log', 'a') as f:
            f.write(f"<{datetime.datetime.now()}> Вызван метод {'{:>16}'.format(func.__name__)} с атрибутами {repr(args)} и ключевыми словами {repr(kwargs)}")
            if type(req) == request.Request:
                f.write(f" от {req.META.get('REMOTE_ADDR')} через {req.META.get('HTTP_X_FORWARDED_FOR')}\n")
            else: f.write(f"\n")
        if args:
            if kwargs:
                return func(*args, **kwargs)
            else: return func(*args)
        elif kwargs:
            return func(**kwargs)
        else: return func()
    return wrapper


@extend_schema_view(
add_pass     =extend_schema(summary='Add new pass to SKUD'           , request=HttpRequest),
repr_pass    =extend_schema(summary='Represent pass in SKUD'         , request=HttpRequest),
repr_passes  =extend_schema(summary='Represent all pass in SKUD'     , request=HttpRequest),
add_door     =extend_schema(summary='Add new door to SKUD'           , request=HttpRequest),
repr_door    =extend_schema(summary='Represent door in SKUD'         , request=HttpRequest),
repr_doors   =extend_schema(summary='Represent all door in SKUD'     , request=HttpRequest),
add_door_pass=extend_schema(summary='Add pass to door & SKUD if none', request=HttpRequest),
remove_pass  =extend_schema(summary='Remove pass from door'          , request=HttpRequest),
)
class SKUDViewSet(ViewSet):
    serializer_class = SKUDSerializer
    
    skudServ = SKUD_Service()
    opServ = OperationsService()

    @action(detail=False)
    def export(self, id:str):
            id = uuid4(id)
            return FileResponse(as_attachment=open(f"{self.opServ.operations.get(id).result}"))

    @action(detail=False)
    def export_logs(self, _):
        operation_id = self.opServ.create_operation()
        print(operation_id)
        scheduler.add_job(self.export_logs_infile, DateTrigger(datetime.datetime.now()), (operation_id, ))
        return HttpResponse(content={'operation_id':operation_id})

    @action(detail=False)
    def export_logs_infile(self, operation_id:UUID):
        name = f"/logs/{datetime.datetime.now()}"
        print(name)
        with open(name, 'w') as f:
            with open("/method_calls.log", 'r') as logs:
                f.write(logs)
        self.opServ.finish_operation(operation_id, name)

    @action(detail=True, methods=['post'])
    def add_pass(self, request): 
        if type(request) == HttpRequest:
            data: dict = json.loads(request.body)
            doorDict = data.get('Door')
            serializer = pasSerializer(data=doorDict)
            print("validated" if serializer.is_valid() else "non-valid", f"pass_id={doorDict.get('UUID')} pass.data")
            pas = serializer.create()
            self.skudServ.add(pas)
            return HttpResponse(content=f"sozdan pass: {self.skudServ.skud.passes.get(pas.id)}")
        elif type(request) == dict:
            serializer = pasSerializer(data=request)
            print("validated" if serializer.is_valid() else "non-valid", f"pass_id={request.get('UUID')} pass.data")
            pas = serializer.create()
            self.skudServ.add(pas)

    @action(detail=True, methods=['get'], url_path='passes/<int:id>')
    def repr_pass(self, request, id):
        if len(self.skudServ.passes_n) > id:
            return HttpResponse(content=f"{self.skudServ.skud.passes.get(self.skudServ.passes_n[id])}")
        else: return HttpResponse(content="No such pass")

    @action(detail=False, methods=['get'], url_path='passes/')
    def repr_passes(self, request):
        return HttpResponse(content=f"{self.skudServ.skud.passes}")
        
    @action(detail=True, methods=['post'])
    def add_door(self, request:HttpRequest):
        data: dict = json.loads(request.body)
        doorDict = data.get('Door')
        if (doorDict.get('allowed') != {}):
            for p in dict(doorDict.get('allowed')).values():
                self.add_pass(p)
        serializer = doorSerializer(data=doorDict)
        print("validated" if serializer.is_valid() else "non-valid", f"door_id={doorDict.get('UUID')} door.data")
        door = serializer.create()
        self.skudServ.add(door)
        return HttpResponse(content=f"sozdan door: {door}")
    
    @action(detail=True, methods=['get'], url_path='doors/<int:id>')
    def repr_door(self, request, id):
        if len(self.skudServ.doors_n) > id:
            return HttpResponse(content=f"{self.skudServ.skud.doors.get(self.skudServ.doors_n[id])}")
        else: return HttpResponse(content="No such pass")

    @action(detail=False, methods=['get'], url_path='doors/')
    def repr_doors(self, request):
        return HttpResponse(content=f"{self.skudServ.skud.doors}")

    @action(detail=True, methods=['post'], url_path='doors/<int:id>/passes')
    def add_door_pass(self, request, id):
        data: dict = json.loads(request.body)
        door1 = self.skudServ.skud.doors.get(id)
        if door1 == None:
            self.add_door(request)
        pass1 = self.skudServ.skud.passes.get(data.get('Pass').get('UUID'))
        if pass1 == None:
            self.add_pass(request)
        self.skudServ.reg(door1,pass1)
        return HttpResponse(content=f"pass {pass1} is \
            added to door {self.skudServ.skud.doors.get(data.get('Door').get('UUID'))}")

    @action(detail=True, methods=['delete'], url_path='doors/<int:id>/passes')
    def remove_passes(self, request):
        data: dict = json.loads(request.body)
        door = self.skudServ.skud.doors.get(data.get("Door").get('UUID'))
        for pas in data.get("Passes"):
            self.skudServ.rem(door, pas)
        self.repr_door(door)

    @action(detail=True, methods=['delete'], url_path='doors/<int:door_id>/passes/<int:pass_id>')
    def remove_pass(self, door_id: int, pass_id: int):
        self.skudServ.skud.doors.get(self.skudServ.doors_n[door_id]).allowed.popitem(self.skudServ.skud.passes.get(self.skudServ.passes_n[pass_id]))

    @action(detail=True, methods=['post'], url_path='check/')
    def check1(self, request):
        data: dict = json.loads(request.body)
        door1 = self.skudServ.skud.doors.get(data.get("Door").get('UUID'))
        if door1 == None:
            self.add_door(request)
        pass1 = self.skudServ.skud.passes.get(data.get('Pass').get('UUID'))
        if pass1 == None:
            self.add_pass(request)
        self.skudServ.check(door1,pass1)
        return HttpResponse(content=f"pass {pass1} is valid to door {door1}")

    @action(detail=True, methods=['get'], url_path='check/<int:door_id>/<int:pass_id>')
    def check2(self, door_id:int, pass_id:int):
        data: dict = json.loads(request.body)
        door1 = self.skudServ.doors_n[door_id]
        pass1 = self.skudServ.passes_n[pass_id]
        self.skudServ.check(door1,pass1)
        return HttpResponse(content=f"pass {pass1} is valid to door {door1}")
        
        
        
        

@extend_schema_view(
    getOperation=extend_schema(summary='Get information about operation', responses=OperationSerializer, auth=False)
)
class OperationViewSet(ViewSet):
    
    OpServ = OperationsService()
        
    @action(detail=True, methods=['get'])
    def getOperation(self, id):
        return self.OpServ.get_operation(id)