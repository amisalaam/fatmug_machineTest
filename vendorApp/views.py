from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor,PurchaseOrder


# Create your views here.


# VENDOR MANAGEMENT
class VendorCreateView(APIView):
    def post(self, request):
        serializer = VendorCreateSerialzers(data=request.data)

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

        serializer = AllVendorSerializers(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

        vendor.delete()
        return Response({"success": "Vendor deleted successfully"}, status=status.HTTP_200_OK)


class PoCreateView(APIView):
    def post(self, request):
        serializer = PoCreateSerializer(data=request.data)

        if serializer.is_valid():
            purchase_order = serializer.save()
            response_data = {
                **serializer.data,
                'po_number': purchase_order.po_number

            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    def get(self,request):
        purachase_order = PurchaseOrder.objects.all()
        serializer = AllPurachaseOrderSerilizer(purachase_order,many=True)

        return Response(serializer.data)
    

class PurchaseOrderDetails(APIView):
    def get(self,request,po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
          return Response({"error": "Purchase not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AllPurachaseOrderSerilizer(purchase_order)

        return Response(serializer.data)
    
    def put(self,request,po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response({"error":"Purchase order not found"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = AllPurachaseOrderSerilizer(purchase_order,data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    
    def delete(self,request,po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response({"error":"Purchase order not found"},status=status.HTTP_404_NOT_FOUND)
        
        purchase_order.delete()
        return Response({"success": "purchase order deleted successfully"}, status=status.HTTP_200_OK)
