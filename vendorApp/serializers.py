from rest_framework import serializers
from .models import Vendor


class VendorSerialzers(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('id','name','contact_details','address')



class AllVendorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields ='__all__'