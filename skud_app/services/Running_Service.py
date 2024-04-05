from uuid import UUID, uuid4
from skud_app.models import Operation
from django.http import HttpResponseNotFound


class OperationsService:
    
    operations: dict[UUID, Operation] = {}
    
    ops_n : Operation = []
    
    def create_operation(self) -> UUID:
        id = uuid4()
        self.operations[id] = Operation(id)
        return id
    def finish_operation(self, id: UUID, result):
        if not id in self.operations:
            return HttpResponseNotFound
        self.operations[id].result = result
        self.operations[id].done   = True
        
    def get_operation(self, id: UUID) -> Operation:
        if not id in self.operations:
            raise HttpResponseNotFound
        return self.operations[id]