import uuid
from rest_framework import serializers
from skud_app.models import *

class pasSerializer(serializers.Serializer):
    
    UUID     = serializers.UUIDField()
    username = serializers.CharField(max_length=100)
    fio      = serializers.CharField(max_length=100)
        
    def create(self) -> Pas:
        return Pas(self.data)

class doorSerializer(serializers.Serializer):
    
    UUID    = serializers.UUIDField()
    cab     = serializers.CharField(max_length=100)
    allowed = serializers.DictField()
    status  = serializers.BooleanField()
    
    def create(self) -> Door:
        return Door(self.data)