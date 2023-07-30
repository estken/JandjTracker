from django.db import models
from .models import JobsModel


# create job history model

class JobHistory(models.Model):
    id = models.AutoField(primary_key=True)
    job_id = models.ForeignKey(JobsModel, on_delete=models.CASCADE, null=False)
    amount_paid = models.FloatField(default= 0.0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.job_id)
    
    