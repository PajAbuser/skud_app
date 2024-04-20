from django.urls import path
from skud_app.views import SKUDViewSet, OperationViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('passes/', SKUDViewSet.as_view({'get':'repr_passes','post':'add_pass'}, name='passseseseseses')),
    path('passes/<int:id>/', SKUDViewSet.as_view({'get':'repr_pass'})),
    path('doors/', SKUDViewSet.as_view({'get':'repr_doors','post':'add_door'})),
    path('doors/<int:id>/', SKUDViewSet.as_view({'get':'repr_door'})),
    path('doors/<int:id>/passes', SKUDViewSet.as_view({'post':'add_door_pass','delete':'remove_passes'})),
    path('doors/<int:door_id>/passes/<int:pass_id>', SKUDViewSet.as_view({'get':'repr_pass','delete':'remove_pass'})),
    path('check/', SKUDViewSet.as_view({'post':'check1'})),
    path('check/<int:door_id>/<int:pass_id>', SKUDViewSet.as_view({'get':'check2'})),
    path('operations/<int:id>', OperationViewSet.as_view({'get':'getOperation'})),
    path('logs/:export', SKUDViewSet.as_view({'get':'export_logs'})),
    path('logs/<str:id>/', SKUDViewSet.as_view({'get':'export'})),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]