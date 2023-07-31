from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
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
@login_required(login_url='/auth_login')
def index(request):
    try:
        if request.user.is_changed:
            messages.add_message(request, messages.INFO,
                                 'Please reset your password')
            return redirect('auth_reset_password')
        
        # required context.
        all_users = ClientUser.objects.all()
        all_complains = JobsModel.objects.all()
        pending = JobsModel.objects.filter(status=False).count()
        completed = JobsModel.objects.filter(status=True).count()
        
        #user_complains = JobsModel.objects.filter(l)
        
        user_context = {
            'user_count': len(all_users),
            'complains': len(all_complains),
            'pend_count': pending,
            'compl_count': completed
        }
            
    except Exception as e:
        messages.add_message(request, messages.WARNING,
                             'An error occurred while creating customer log')
        return redirect('index')
        
    return render(request, 'Trackerfolder/index.html', user_context)

@login_required(login_url='/auth_login')
def create_log(request):
    try:
        field_check = True
        if request.user.is_changed:
            messages.add_message(request, messages.INFO,
                                 'Please reset your password')
            return redirect('auth_reset_password')
        
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
                    request, messages.WARNING, 'Phone number must contain a valid country code')
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
        messages.add_message(request, messages.WARNING,
                             'An error occurred while creating customer log')
        return redirect('log_complain')
    template_name = 'Trackerfolder/log_complain.html'
    return render(request, template_name)

@login_required(login_url='/auth_login')
def log_out(request):
    logout(request)
    # will be changed to the login view though.
    return redirect('auth_login')

def auth_login(request):
    try:
        if request.method == "POST":
            user_mail = request.POST.get('email', '')
            user_password = request.POST.get('password', '')
            
            user = authenticate(request, email=user_mail, password=user_password)
            # if it's not None, it means the user details was correct.
            if user is not None:
                # check if the user is required to change their password.
                login(request, user)
                if user.is_changed:
                    
                    messages.add_message(request, messages.INFO,
                                         'Please reset your password')
                    return redirect('auth_reset_password')
                # login.
                next_page = request.GET.get('next', None)
                # if the user was trying to access a page that requires authentication,
                # then redirect back to that page of the website
                if next_page is not None:
                    return redirect(next_page)
                return HttpResponseRedirect(reverse('index'))
            else:
                messages.add_message(
                    request, messages.WARNING, 'Invalid username or password!')
                
                return HttpResponseRedirect(reverse('auth_login'))
            
    except Exception as e:
        messages.add_message(request, messages.WARNING,
                             'An error occurred while trying to login')
        return redirect('auth_login')
        
    return render(request, 'Trackerfolder/auth-login.html')

@login_required(login_url='/auth_login')
def auth_reset_password(request):
    try:
        if not request.user.is_changed:    
            return redirect('auth_login')
        if request.method == "POST":
            fpassword = request.POST.get('pass', '')
            cpassword = request.POST.get('password', '')
            
            if fpassword != cpassword:
                messages.add_message(request, messages.WARNING,
                             'Password do not match')
                return redirect('auth_reset_password')
            
            user = ClientUser.objects.get(email = request.user.email)
            user.set_password(fpassword)
            user.is_changed = False
            
            user.save()
            login(request, user)
            next_page = request.GET.get('next', None)
            # if the user was trying to access a page that requires authentication,
            # then redirect back to that page of the website
            if next_page is not None:
                return redirect(next_page)
            return HttpResponseRedirect(reverse('index'))
    
    except Exception as e:
        messages.add_message(request, messages.WARNING,
                             'An error occurred while trying to reset password')
        return redirect('auth_reset_password')
        
        
    return render(request, 'Trackerfolder/auth-reset-password.html')

def profile(request):
    
    return render(request, 'Trackerfolder/features-profile.html')
