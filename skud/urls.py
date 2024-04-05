from django.urls import path
from skud_app.views import SKUDViewSet

urlpatterns = [
    path('passes/', SKUDViewSet.as_view({'get':'create_SKUD','post':'add_pass'}, name='passseseseseses')),
    path('doors/', SKUDViewSet.as_view({'post':'add_door'})),
    path('doors/<id>/passes', SKUDViewSet.as_view({'post':'add_door_pass'})),
]