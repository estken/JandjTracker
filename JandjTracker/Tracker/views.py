from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from .utils import *
from django.contrib import messages
from django.contrib.messages import constants as cs
from .models import *
from .log_history_model import *
from .job_history_model import *

MESSAGE_TAGS = {
    cs.ERROR: 'danger'
}

# Create your views here.
def index(request):
    return render(request, 'Trackerfolder/index.html')

def create_log(request):
    try:
        field_check = True
        if request.method == "POST":
            full_name = request.POST.get('full_name', '')
            phone_number = request.POST.get('phone', '')
            gender = request.POST.get('gender', '')
            amount = request.POST.get('amount', '')
            complain_date = request.POST.get('complain_date', '')
            complain_message = request.POST.get('message', '')
            check_number = has_country_code(phone_number)
            if not check_number:
                field_check = False
                messages.add_message(
                    request, messages.ERROR, 'Phone number must contain a valid country code')
            if field_check:
                # create the complain
                new_complain = JobsModel.objects.create(
                    clients_name = full_name,
                    complains = complain_message,
                    payments = amount,
                    gender = gender,
                    phone_number = phone_number,
                    logged_at = complain_date,
                    log_by = request.user.username
                )
                LogHistoryModel.objects.create(job_id=new_complain, updated_by=request.user.username)
                JobHistory.objects.create(job_id = new_complain)
                messages.add_message(request, messages.SUCCESS, 
                                     f'Complain for {full_name} was successfully logged.')
            
            return redirect('log_complain')
        
    except Exception as e:
        print(str(e))
        messages.add_message(request, messages.ERROR,
                             'An error occurred while creating customer log')
        return redirect('log_complain')
    template_name = 'Trackerfolder/log_complain.html'
    return render(request, template_name)

@login_required(login_url='')
def log_out(request):
    logout(request)
    # will be changed to the login view though.
    return redirect('index')