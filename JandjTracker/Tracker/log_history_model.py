from django.db import models
from .models import JobsModel



# create log history models

class LogHistoryModel(models.Model):
    
    id = models.AutoField(primary_key=True)
    job_id = models.ForeignKey(JobsModel, on_delete=models.CASCADE, null=False)
    updated_by = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.updated_by
    