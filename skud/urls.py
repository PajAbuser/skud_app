from django.urls import path
from skud_app.views import SKUDViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('passes/', SKUDViewSet.as_view({'get':'repr_passes','post':'add_pass'}, name='passseseseseses')),
    path('passes/<int:id>/', SKUDViewSet.as_view({'get':'repr_pass'})),
    path('doors/', SKUDViewSet.as_view({'get':'repr_doors','post':'add_door'})),
    path('doors/<int:id>/', SKUDViewSet.as_view({'get':'repr_door'})),
    path('doors/<int:id>/passes', SKUDViewSet.as_view({'post':'add_door_pass','delete':'remove_pass'})),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),

]