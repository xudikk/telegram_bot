from django.urls import path
from .v1.views import RegionListView, DistrictListView

urlpatterns = [
    path('regions/', RegionListView.as_view(), name='regions-list-v1'),
    path('districts/<int:id>/', DistrictListView.as_view(), name='districts-list-v1')

]
