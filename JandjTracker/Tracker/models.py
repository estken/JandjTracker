from django.db import models
from .user_model import ClientUser
import uuid
from datetime import datetime

# Create your models here.


class JobsModel(models.Model):
    id = models.AutoField(primary_key=True)
    client_id = models.UUIDField(default=uuid.uuid4, editable = False, unique=True)
    clients_name = models.CharField(max_length=100, null=True)
    payments = models.FloatField(null=True, default= 0.0)
    company_name = models.CharField(max_length=50, null=True)
    job_description = models.TextField(null=True)
    payments = models.BooleanField(default=False)
    status = models.BooleanField(default=False, null=True)
    log_by = models.CharField(max_length=50)
    answer_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=15)  # Adjust the max_length as needed
    logged_at = models.DateTimeField(default = datetime.now())
    
    def __str__(self):
        return self.clients_name
    
