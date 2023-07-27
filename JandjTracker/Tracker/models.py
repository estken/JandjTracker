from django.db import models
import uuid

# Create your models here.


class Jobs(models.Model):
    id = models.AutoField(primary_key=True)
    client_id = models.UUIDField(default=uuid.uuid4, editable = False, unique=True)
    clients_name = models.CharField(max_length=100)
    complains = models.TextField(null=True)
    payments = models.FloatField(null=True)
    status = models.BooleanField(default=False, null=True)
    log_by = models.CharField(max_length=50)
    answer_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
    def __str__(self):
        return self.clients_name
    
