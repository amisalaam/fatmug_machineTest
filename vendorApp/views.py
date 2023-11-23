from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import VendorSerialzers, AllVendorSerializers
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor


# Create your views here.

class VendorCreateView(APIView):
    def post(self, request):
        serializer = VendorSerialzers(data=request.data)

        if serializer.is_valid():
            vendor = serializer.save()
            response_data = {
                **serializer.data,
                'vendor_code': vendor.vendor_code,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = AllVendorSerializers(vendors, many=True)

        return Response(serializer.data)


class VenodrDetailsView(APIView):
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found "}, status=status.HTTP_404_NOT_FOUND)

        serializer = AllVendorSerializers(vendor)

        return Response(serializer.data)


    def put(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = VendorSerialzers(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

        vendor.delete()
        return Response({"success":"Vendor deleted successfully"},status=status.HTTP_204_NO_CONTENT)
    


