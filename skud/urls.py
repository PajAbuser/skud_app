from django.urls import path
from skud_app.views import SKUDViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('passes/', SKUDViewSet.as_view({'get':'create_SKUD','post':'add_pass'}, name='passseseseseses')),
    path('doors/', SKUDViewSet.as_view({'post':'add_door'})),
    path('doors/<id>/passes', SKUDViewSet.as_view({'post':'add_door_pass'})),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),

]