from django.urls import path
from .views import *

urlpatterns = [
    path('vendors/', VendorCreateView.as_view(), name='vendor-create'),
    path('vendors/<int:vendor_id>/', VenodrDetailsView.as_view(), name='vendor-detail'),

    path('purchase_order/', PoCreateView.as_view(), name='order-create'),
    path('purchase_order/<int:po_id>/', PurchaseOrderDetails.as_view(), name='order-detail'),

    path('vendors/<int:vendor_id>/performance/', PerfomanceMetricsAPIView.as_view(), name='vendor_performance'),


]
