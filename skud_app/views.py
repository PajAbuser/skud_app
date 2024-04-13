import datetime
import inspect
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
from skud_app.scheduler import scheduler, DateTrigger, CronTrigger
from functools import wraps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import viewsets
from skud_app.tests import unit, e2e


# def log_method_calls(log_file):
#     def decorator(cls):
#         for name, method in inspect.getmembers(cls, inspect.isfunction):
#             @functools.wraps(method)
#             def wrapper(self, *args, **kwargs):
#                 if len(args) > 0: req  = args[0]
#                 else: req = args
#                 with open("method_calls.log", 'a') as f:
#                     f.write(f"<{datetime.datetime.now()}> Invoked method {'{:>16}'.format(method.__name__)} with args {repr(args)} and keywords {repr(kwargs)}")
#                     if type(req) == request.Request:
#                         f.write(f" from {req.META.get('REMOTE_ADDR')} through {'localhost' if req.META.get('HTTP_X_FORWARDED_FOR') == None else req.META.get('HTTP_X_FORWARDED_FOR')}" + '\n')
#                     else: f.write(f"\n")
#                 if name == 'throttled': return method(self, HttpRequest(), wait=10)
#                 else: return method(self, *args, **kwargs)
#             setattr(cls, name, wrapper)
#         return cls
#     return decorator

# def log_method_calls(cls):
#     print("in decorator")
#     # inspect.getargs(cls)
#     class Wrapper(cls):
#         for name, method in inspect.getmembers(cls,inspect.isfunction):
#             print("in hz",name,method)
#             @functools.wraps(method)
#             def dispatch(self, *args, **kwargs):
#                 if(args): req = args[1]
#                 with open("method_calls.log", 'w') as f:
#                         f.write(f"<{datetime.datetime.now()}> Invoked method {'{:>16}'.format(super.name)} with args {repr(args)} and keywords {repr(kwargs)}")
#                         if type(req) == request.Request:
#                             f.write(f" from {req.META.get('REMOTE_ADDR')} through {'localhost' if req.META.get('HTTP_X_FORWARDED_FOR') == None else req.META.get('HTTP_X_FORWARDED_FOR')}" + '\n')
#                         else: f.write(f"\n")
#     return Wrapper
#     # def wrap(self, request, *args, **kwargs):
#     #     # Получаем имя вызываемого метода
#     #     method_name = request.method.lower()
        
#     #     # Получаем вызываемый метод класса
#     #     method = getattr(self, method_name, None)
        
#     #     if method is None:
#     #         # Если метод не найден, возвращаем ошибку 405 (Method Not Allowed)
#     #         return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
#     #     # Создаем словарь с информацией о вызове метода
#     #     # method_info = {
#     #     #     'method_name': method_name,
#     #     #     'args': args,
#     #     #     'kwargs': kwargs
#     #     # }
        
#     #     # Записываем информацию о вызове метода в файл
#     #     req = args
        
def log_method_calls(cls):

    # Получить имя класса
    class_name = cls.__name__

    # Обернуть все методы класса
    for name, method in cls.__dict__.items():
        if callable(method):
            # Обернуть метод
            @functools.wraps(method)
            def wrapper(self, *args, **kwargs):
                # Залогировать вызов метода
                if len(args) > 0: req  = args[0]
                else: req = args
                with open("method_calls.log", 'a') as f:
                    f.write(f"<{datetime.datetime.now()}> Invoked method {'{:>16}'.format(method.__name__)} with args {repr(args)} and keywords {repr(kwargs)}")
                    if type(req) == request.Request:
                        f.write(f" from {req.META.get('REMOTE_ADDR')} through {'localhost' if req.META.get('HTTP_X_FORWARDED_FOR') == None else req.META.get('HTTP_X_FORWARDED_FOR')}" + '\n')
                    else: f.write(f"\n")

                # Вызвать оригинальный метод
                return method(self, *args, **kwargs)

            # Заменить оригинальный метод обернутым
            setattr(cls, name, wrapper)

    # Вернуть декорированный класс
    return cls

@extend_schema_view(
add_pass          =extend_schema(summary='Add new pass to SKUD'           , request=HttpRequest),
repr_pass         =extend_schema(summary='Represent pass in SKUD'         , request=HttpRequest),
repr_passes       =extend_schema(summary='Represent all pass in SKUD'     , request=HttpRequest),
add_door          =extend_schema(summary='Add new door to SKUD'           , request=HttpRequest),
repr_door         =extend_schema(summary='Represent door in SKUD'         , request=HttpRequest),
repr_doors        =extend_schema(summary='Represent all door in SKUD'     , request=HttpRequest),
add_door_pass     =extend_schema(summary='Add pass to door & SKUD if none', request=HttpRequest),
remove_pass       =extend_schema(summary='Remove pass from door'          , request=HttpRequest),
export            =extend_schema(summary='Get log by operation id'        , request=HttpRequest),
export_logs_infile=extend_schema(summary='Get logs exported in file'      , request=HttpRequest),
)
# @log_method_calls
class SKUDViewSet(ViewSet):
    serializer_class = SKUDSerializer
    
    skudServ = SKUD_Service()
    opServ = OperationsService()
    
    @action(detail=False)
    def export(self, request, id:str):
            id = UUID(id)
            if self.opServ.operations.get(id).done:
                return FileResponse(open(self.opServ.operations.get(id).result, 'rb'))
            else: return HttpResponse(content="Operation is still running")

    @action(detail=False)
    def export_logs(self, request):
        operation_id = self.opServ.create_operation()
        scheduler.add_job(self.export_logs_infile, trigger=DateTrigger(datetime.datetime.now()), args=(operation_id, ))
        if not scheduler.running: scheduler.start()
        return HttpResponse(JsonResponse({'operation_id':operation_id}))

    @action(detail=False)
    def export_logs_infile(self, operation_id:UUID):
        name = "logs/" + f"{str(datetime.datetime.now()).replace(' ','-').replace(':','-').replace('.','-')}.log"
        with open(name, 'w+') as f:
            with open(f"method_calls.log", 'r') as logs:
                for l in logs:
                    f.write(l)
        self.opServ.finish_operation(operation_id, name)
        
        # print("ended operation - ",self.opServ.get_operation(operation_id))

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
        return self.skudServ.check(door1,pass1)

    @action(detail=True, methods=['get'], url_path='check/<int:door_id>/<int:pass_id>')
    def check2(self, door_id:int, pass_id:int):
        data: dict = json.loads(request.body)
        door1 = self.skudServ.doors_n[door_id]
        pass1 = self.skudServ.passes_n[pass_id]
        self.skudServ.check(door1,pass1)
        return HttpResponse(content=f"pass {pass1} is valid to door {door1}")
        
    @action(detail=True, methods=['get'], url_path='tests/unit')
    def test_unit(self, req):
        for method in inspect.getmembers(unit.UnitTest, inspect.isfunction):
            exec(method)
    
    @action(detail=True, methods=['get'], url_path='tests/e2e')
    def test_e2e(self, req):
        for method in inspect.getmembers(e2e.E2ETests, inspect.isfunction):
            exec(method)
        
        
        

@extend_schema_view(
    getOperation=extend_schema(summary='Get information about operation', responses=OperationSerializer, auth=False)
)
class OperationViewSet(ViewSet):
    
    OpServ = OperationsService()
        
    @action(detail=True, methods=['get'])
    def getOperation(self, id):
        return self.OpServ.get_operation(id)