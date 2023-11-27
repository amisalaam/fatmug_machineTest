from django.db import models
import random
import string
from django.db.models import Avg, F
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(blank=True, null=True)
    quality_rating_avg = models.FloatField(blank=True, null=True)
    average_response_time = models.FloatField(blank=True, null=True)
    fulfillment_rate = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.vendor_code and not self.pk:
            self.vendor_code = self.generate_unique_vendor_code()

        super().save(*args, **kwargs)

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
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    status_date = models.DateTimeField(null=True, blank=True)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def generate_unique_po_number(self):
        random_part = ''.join(random.choices(string.digits, k=5))
        return f'ORDER{random_part}'

    def save(self, *args, **kwargs):
        if not self.po_number:
            self.po_number = self.generate_unique_po_number()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"PO {self.po_number} - {self.vendor.name}"
    

@receiver(pre_save, sender=PurchaseOrder)
def update_status_date(sender, instance, **kwargs):
    if instance.status == 'completed' and not instance.status_date:
        instance.status_date = timezone.now()


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    average_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)

    def calculate_and_save_metrics(self):
        completed_pos = PurchaseOrder.objects.filter(vendor=self.vendor, status='completed')
        total_completed_pos = completed_pos.count()

        on_time_deliveries = completed_pos.filter(status_date__lte=F('delivery_date'))
        on_time_delivery_rate = on_time_deliveries.count() / completed_pos.count() if completed_pos.count() > 0 else 0

        quality_rating_avg = completed_pos.aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating'] or 0

        acknowledged_pos = completed_pos.exclude(acknowledgment_date=None)
        avg_response_time = acknowledged_pos.aggregate(avg_response_time=Avg(F('acknowledgment_date') - F('issue_date')))['avg_response_time'] or 0

        successful_fulfillments = completed_pos.filter(acknowledgment_date__isnull=False, issue_date__lte=timezone.now())
        fulfillment_rate = successful_fulfillments.count() / completed_pos.count() if completed_pos.count() > 0 else 0

        self.on_time_delivery_rate = on_time_delivery_rate
        self.quality_rating_avg = quality_rating_avg
        self.average_response_time = avg_response_time
        self.fulfillment_rate = fulfillment_rate

        self.save()

    def __str__(self):
        return f"History {self.vendor.name}"
