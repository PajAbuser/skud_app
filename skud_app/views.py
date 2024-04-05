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


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # req: WSGIRequest = make_middleware_aware(args[1])
        # req1: HttpRequest
        req  = args[1]
        # Записать в файл информацию о вызове метода
        with open('method_calls.log', 'a') as f:
            f.write(f"<{datetime.datetime.now()}> Вызван метод {func.__name__} с аргументами {repr(args)} и ключевыми словами {repr(kwargs)}")
            if type(req) == request.Request:
                f.write(f" от {req.META.get('REMOTE_ADDR')} через {req.META.get('HTTP_X_FORWARDED_FOR')}\n")
            else: f.write(f"\n")

        # Вызвать исходный метод
        return func(*args, **kwargs)
    return wrapper


@extend_schema_view(
# list=extend_schema(summary='Applications list', parameters=[     ], auth=False), # serializer tooda

add_pass=extend_schema(summary='Add new pass to SKUD', request=HttpRequest),
add_door=extend_schema(summary='Add new door to SKUD', request=HttpRequest),
add_door_pass=extend_schema(summary='Add pass to door & SKUD if none', request=HttpRequest),

#get_one=extend_schema(summary='One application', description='Allows to get one application by it\'s ID or returns error')
)
class SKUDViewSet(ViewSet):
    serializer_class = SKUDSerializer
    
    skudServ = SKUD_Service()
    @log
    def create_SKUD(self, request):
        return self.skudServ.create()
    
    @log
    @action(detail=True, methods=['post'])
    def add_pass(self, request): 
        if type(request) == HttpRequest:
            data: dict = json.loads(request.body)
            doorDict = data.get('Door')
            serializer = pasSerializer(data=doorDict)
            print("validated" if serializer.is_valid() else "non-valid", f"pass_id={doorDict.get('UUID')} pass.data")
            pas = serializer.create()
            self.skudServ.add(pas)
            return HttpResponse(content=f"sozdan pass: {self.skudServ.skuds.get(data.get('skud_id')).passes.get(pas.id)}")
        elif type(request) == dict:
            serializer = pasSerializer(data=request)
            print("validated" if serializer.is_valid() else "non-valid", f"pass_id={request.get('UUID')} pass.data")
            pas = serializer.create()
            self.skudServ.add(pas)
    
    @log
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

    @log
    @action(detail=True, methods=['post'])
    def add_door_pass(self, request, id:UUID):
        data: dict = json.loads(request.body)
        skud_id = data.get('skud_id')
        door1 = self.skudServ.skuds.get(skud_id).doors.get(id)
        if door1 == None:
            self.add_door(request)
        pass1 = self.skudServ.skuds.get(skud_id).passes.get(data.get('Pass').get('UUID'))
        if pass1 == None:
            self.add_pass(request)
        self.skudServ.reg(door1,pass1, skud_id)
        return HttpResponse(content=f"pass {pass1} is \
            added to door {self.skudServ.skuds.get(skud_id).doors.get(data.get('Door').get('UUID'))}")
            
    def _add(self, request):
        data: dict = json.loads(request.body)
        return HttpResponse(content="")
        
    def _add(self, request):
        data: dict = json.loads(request.body)
        return HttpResponse(content="")
        
    def _add(self, request):
        data: dict = json.loads(request.body)
        return HttpResponse(content="")
        
    def _add(self, request):
        data: dict = json.loads(request.body)
        return HttpResponse(content="")

    def _add(self, request):
        data: dict = json.loads(request.body)
        return HttpResponse(content="")
        
    def _add(self, request):
        data: dict = json.loads(request.body)
        return HttpResponse(content="")
        
    def _add(self, request):
        data: dict = json.loads(request.body)
        return HttpResponse(content="")
        
    def _add(self, request):
        data: dict = json.loads(request.body)  
        return HttpResponse(content="")
    