import json
import uuid
from django.http import HttpResponse, JsonResponse, FileResponse, HttpRequest
from rest_framework import serializers
from skud_app.models import *


class PasSerializer(serializers.Serializer):
    
    id       = serializers.UUIDField()
    username = serializers.CharField(max_length=100)
    fio      = serializers.CharField(max_length=100)

    def create(self) -> Pas:
        pas = Pas(self.validated_data)
        return pas


class PasDictSerializer(serializers.Serializer):
    
    passes = PasSerializer(many=True)

    def create(self):
        passes = []
        for pas_data in self.data['passes']:
            pas_serializer = PasSerializer(data=pas_data)
            pas_serializer.is_valid()
            pas = pas_serializer.create()
            passes.append(pas)
        return passes


class DoorSerializer(PasDictSerializer):
    
    id     = serializers.UUIDField   ()
    cab    = serializers.CharField   (max_length=100)
    status = serializers.BooleanField(default=True)

    def create(self):
        validated_data = self.validated_data
        pas = PasDictSerializer(data=self.validated_data)
        print('pas.is_valid() =', pas.is_valid())
        passes = pas.create()
        validated_data.update({'passes':passes})
        door = Door(validated_data)
        return door


class DoorDictSerializer(serializers.Serializer):
    
    doors = DoorSerializer(many=True)
    
    def create(self):
        doors = []
        for door_data in self.validated_data['doors']:
            door_serializer = DoorSerializer(data=door_data)
            door_serializer.is_valid()
            door = door_serializer.create()
            doors.append(door)
        return doors


class SKUDSerializer(PasDictSerializer, DoorDictSerializer):
    
    class Meta:
        inherit = False


class OperationSerializer(serializers.Serializer):
    
    id     = serializers.UUIDField   ()
    done   = serializers.BooleanField()
    result = serializers.JSONField   (default={})
