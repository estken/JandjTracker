from django.db import models
from models import Jobs



# create payments model


class PaymentsModel(models.Model):
    id = models.AutoField(primary_key=True)
    total_payments = models.FloatField(null=True)
    amount_paid = models.FloatField(null=True)
    pending_amount = models.FloatField(null=True)
    jobs_id = models.ForeignKey(Jobs, on_delete=models.CASCADE, null=False)
    