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

