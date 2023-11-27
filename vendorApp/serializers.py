from rest_framework import serializers
from .models import Vendor,PurchaseOrder,HistoricalPerformance


class VendorCreateSerialzers(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('id','name','contact_details','address')


class AllVendorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        exclude = ['vendor_code']


class PoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ('id','vendor','delivery_date','items','quantity')


class AllPurachaseOrderSerilizer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        exclude = ['po_number']


class PerfomanceMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'