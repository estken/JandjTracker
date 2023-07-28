from django.contrib import admin
from .models import JobsModel
from .job_history_model import JobHistory
from .payments_model import PaymentsModel
from .log_history_model import LogHistoryModel

# Register your models here.

admin.site.register(JobsModel)
admin.site.register(JobHistory)
admin.site.register(PaymentsModel)
admin.site.register(LogHistoryModel)
