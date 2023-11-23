from django.urls import path
from .views import VendorCreateView

urlpatterns = [
    path('api/vendors/', VendorCreateView.as_view(), name='vendor-create')
    
]
