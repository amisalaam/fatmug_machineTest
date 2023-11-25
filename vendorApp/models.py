from django.db import models
import random
import string

# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50,unique=True)
    on_time_delivery_rate = models.FloatField(blank=True,null=True)
    quality_rating_avg = models.FloatField(blank=True,null=True)
    average_response_time = models.FloatField(blank=True,null=True)
    fulfillment_rate = models.FloatField(blank=True,null=True)

    def save(self, *args, **kwargs):
        if not self.vendor_code and not self.pk:
            self.vendor_code = self.generate_unique_vendor_code()

        super().save(*args, **kwargs)

    #CREATING UNIQUE VENDOR CODE AUTOMATICALLY TO MAKE USER FRIENDLY
    def generate_unique_vendor_code(self):
        prefix = 'VENDOR'
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return f'{prefix}_{random_part}'
    
    def __str__(self):
        return self.name



class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES,default= 'pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)


    #CREATING UNIQUE PO NUMBER AUTOMATICALLY TO MAKE USER FRIENDLY
    def generate_unique_po_number(self):
        random_part = ''.join(random.choices(string.digits, k=5)) 
        return f'ORDER{random_part}'
    
    def save(self, *args, **kwargs):
        if not self.po_number:
            self.po_number = self.generate_unique_po_number()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"PO {self.po_number} - {self.vendor.name}"