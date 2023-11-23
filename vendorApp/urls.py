from django.urls import path
from .views import VendorCreateView,VenodrDetailsView

urlpatterns = [
    path('api/vendors/', VendorCreateView.as_view(), name='vendor-create'),
    path('api/vendors/<int:vendor_id>/', VenodrDetailsView.as_view(), name='vendor-detail'),
]
