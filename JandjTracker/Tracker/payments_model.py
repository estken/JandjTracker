from django.db import models
from .models import JobsModel
from datetime import datetime

# create payments model
class PaymentsModel(models.Model):
    id = models.AutoField(primary_key=True)
    total_payments = models.FloatField(null=True)
    amount_paid = models.FloatField(null=True)
    pending_amount = models.FloatField(null=True)
    jobs_id = models.ForeignKey(JobsModel, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(default=datetime.now())
  
    def __str__(self):
        return self.total_payments
    