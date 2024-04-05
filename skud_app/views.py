import io
from django.http import HttpResponse, JsonResponse, FileResponse, HttpRequest
import json
from django.views.decorators.csrf import csrf_exempt
from skud_app.models import *
from skud_app.serializers import *
from rest_framework.viewsets import ViewSet
from skud_app.services.SKUD_Service import SKUD_Service
from rest_framework.parsers import JSONParser
from drf_spectacular.utils import extend_schema, extend_schema_view


skudServ = SKUD_Service()

@extend_schema_view(
list=extend_schema(summary='Applications list', parameters=[     ], auth=False), # serializer tooda
create=extend_schema(summary='New applicationn',
request=None), # i tooda
get_one=extend_schema(summary='One application', description='Allows to get \
one application by it\'s ID or returns error')
)
class SKUDViewSet(ViewSet):
    
    def create_SKUD(self, request):
        return skudServ.create()
        
    def add_pass(self, request): 
        if type(request) == HttpRequest:
            data: dict = json.loads(request.body)
            doorDict = data.get('Door')
            serializer = pasSerializer(data=doorDict)
            print("validated" if serializer.is_valid() else "non-valid", f"pass_id={doorDict.get('UUID')} pass.data")
            pas = serializer.create()
            skudServ.add(pas)
            return HttpResponse(content=f"sozdan pass: {skudServ.skuds.get(data.get('skud_id')).passes.get(pas.id)}")
        elif type(request) == dict:
            serializer = pasSerializer(data=request)
            print("validated" if serializer.is_valid() else "non-valid", f"pass_id={request.get('UUID')} pass.data")
            pas = serializer.create()
            skudServ.add(pas)
                
    def add_door(self, request:HttpRequest):
        data: dict = json.loads(request.body)
        doorDict = data.get('Door')
        if (doorDict.get('allowed') != {}):
            for p in dict(doorDict.get('allowed')).values():
                self.add_pass(p)
        serializer = doorSerializer(data=doorDict)
        print("validated" if serializer.is_valid() else "non-valid", f"door_id={doorDict.get('UUID')} door.data")
        door = serializer.create()
        skudServ.add(door)
        return HttpResponse(content=f"sozdan door: {door}")

        
    def add_door_pass(self, request, id:UUID):
        data: dict = json.loads(request.body)
        skud_id = data.get('skud_id')
        door1 = skudServ.skuds.get(skud_id).doors.get(id)
        if door1 == None:
            self.add_door(request)
        pass1 = skudServ.skuds.get(skud_id).passes.get(data.get('Pass').get('UUID'))
        if pass1 == None:
            self.add_pass(request)
        skudServ.reg(door1,pass1, skud_id)
        return HttpResponse(content=f"pass {pass1} is \
            added to door {skudServ.skuds.get(skud_id).doors.get(data.get('Door').get('UUID'))}")
            
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
    