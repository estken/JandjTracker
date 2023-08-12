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
from django.utils.html import format_html
from django.core.paginator import Paginator


MESSAGE_TAGS = {
    cs.ERROR: 'danger'
}

# Create your views here.
def error_404(request, exception):
    return render(request, 'Trackerfolder/error404.html')

def error_500(request, *args, **argv):
    return render(request, 'Trackerfolder/error500.html', status=500)


@login_required(login_url='/auth_login')
def index(request):
    try:
        if request.user.is_changed:
            messages.add_message(request, messages.INFO,
                                 'Please reset your password')
            return redirect('auth_reset_password')
        
        # required context.
        pending_jobs = JobsModel.objects.filter(status=False).count()
        completed_jobs = JobsModel.objects.filter(status=True).count()
        pending_payments = JobsModel.objects.filter(payments=True, status=False).count()
        settled_payments = JobsModel.objects.filter(payments=True, status=True).count()        
        
        user_context = {
            'pend_count': pending_jobs,
            'compl_count': completed_jobs,
            'pending_payments':pending_payments,
            'settled_payments' : settled_payments,
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
            company_name = request.POST.get('company_name', '')
            phone_number = request.POST.get('phone_number', '')
            answer_at = request.POST.get('complain_date', '')
            payment = request.POST.get('payment', '')
            if payment.lower() == "false":
                get_payment = False
            else:
                get_payment = True
            job_description = request.POST.get('job_description', '')
            check_number = has_country_code(phone_number)
            if not check_number:
                field_check = False
                messages.add_message(
                    request, messages.WARNING, 'Phone number must contain a valid country code')
            if field_check:
                # create the complain
                new_complain = JobsModel.objects.create(
                    clients_name = full_name,
                    company_name = company_name,
                    job_description = job_description,
                    phone_number = phone_number,
                    logged_at = answer_at,
                    log_by = request.user.username,
                    payments = get_payment
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

@login_required(login_url='/auth_login')
def profile(request):
    if request.method == 'POST':
        password = request.POST['password']
        new_pass = request.POST['password']
        current_pass =request.POST['password']
        if new_pass != current_pass:
            messages.add_message(request, messages.WARNING, 'password does not match')
        pass_reset = ClientUser.objects.get(email = request.user.email)
        pass_reset.set_password(password)
        
        
        pass_reset.save()
        messages.add_message(request, messages.SUCCESS, 'Password Change Successfully.')
            
        
    return render(request, 'Trackerfolder/features-profile.html')

def profile_details(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        
        
        my_profile = ClientUser.objects.filter(email = email).first()
        print(my_profile)
        if my_profile is not None:
            messages.add_message(request, messages.WARNING, 'email already exits.')
            return redirect('profile')
        my_profile = ClientUser.objects.get(email = request.user.email)   
        my_profile.email = email    
        my_profile.name = name

        my_profile.save()
        messages.add_message(request, messages.SUCCESS, 'email change successfully.')
        return redirect('profile')
    
    
def pending_complains(request):
  
    pen_complains = JobsModel.objects.all()
    
    context = {
        'pen_complains':pen_complains
    }
    return render(request, 'Trackerfolder/pending-complains.html', context)


def review_complains(request, id):
    get_review = JobsModel.objects.get(id=id)
    context = {
        'get_review': get_review,
    }
    return render(request, 'Trackerfolder/review_complain.html', context)


def detail_review_complains(request, id):
    if request.method == 'POST':
        clients_name = request.POST['clients_name']
        phone_number = request.POST['phone_number']
        gender = request.POST['gender']
        payments = request.POST['payments']
        complains = request.POST['complains']
        
        get_review = JobsModel.objects.get(id=id)
        get_review.clients_name = clients_name
        get_review.phone_number = phone_number
        get_review.gender = gender
        get_review.payments = payments
        get_review.complains = complains
        
        get_review.save()
    messages.add_message(request, messages.SUCCESS, 'Details updated successfully')    
    return redirect('review_complains', id)


def client_delete(request, id):
    get_review = JobsModel.objects.get(id=id)
    if request.method == 'POST':
        get_review.delete()
        return redirect('pending_complains')    
    context = {
        'del_client':get_review
    }
    return redirect('pending_complains',context)


def all_complains(request):
    try:
        
        a_complains = JobsModel.objects.all().order_by('-created_at')
        pending = JobsModel.objects.filter(status=False).count()
        completed = JobsModel.objects.filter(status=True).count()
        
        items_per_page = 10
        pagine = Paginator(a_complains, items_per_page)
        # get the page number.
        page_numb = request.GET.get('page')
        page = pagine.get_page(page_numb)
        
    
        context = {
            'all': len(a_complains),
            'pending': pending,
            'completed': completed,
            'page': page
        }
        
    except Exception as e:
        messages.add_message(request, messages.WARNING,
                             'An error occurred while trying to fetch records')
        return redirect('all_complains')
    
    return render(request, 'Trackerfolder/all_complain.html', context)


def activities(request):
    get_all_activities = JobsModel.objects.all()[:10]
    
    context = {
        'get_all_activities' : get_all_activities
    }
    return render(request, 'Trackerfolder/features-activities.html', context)



def view_activity(request, id):
    pen_complains = JobsModel.objects.filter(id=id)
    
    context = {
        'pen_complains':pen_complains
    }
    return render(request, 'Trackerfolder/activities-view.html', context)


def del_activities(request, id):
    get_all_activities = JobsModel.objects.get(id=id)
    if request.method == 'POST':
        get_all_activities.delete()
        return redirect('pending_complains')    
    context = {
        'get_all_activities':get_all_activities
    }
    
    return redirect('activities', context)

@login_required(login_url='/auth_login')
def edit_complains(request, pk):
    try:
        field_check = True
        complain = get_object_or_404(JobsModel, pk=pk)
        # check if the user is the one that actually logged the complain.
        if not (request.user.username==complain.log_by):
            messages.add_message(request, messages.WARNING,
                                 f'you are not authorized to edit this complain, because it wasnot logged by you. It was logged by {complain.log_by}')
            redirect('index')
            
        if request.method == "POST": 
            full_name = request.POST.get('full_name', '')
            comp_name = request.POST.get('comp_name', '')
            phone_number = request.POST.get('phone', '')
            payment = request.POST.get('payment', '')
            if payment.lower() == "no":
                get_payment = False
            else:
                get_payment = True
            complain_date = request.POST.get('complain_date', '')
            complain_message = request.POST.get('message', '')
            check_number = has_country_code(phone_number)
        
            if not check_number:
                field_check = False
                messages.add_message(
                    request, messages.WARNING, 'Phone number must contain a valid country code')
        
            if field_check:
                # create the complain
                complain.clients_name = full_name
                complain.job_description = format_html(complain_message)
                complain.payments = get_payment
                complain.phone_number = phone_number
                complain.logged_at = complain_date
                complain.company_name = comp_name
                # save.
                complain.save()
                messages.add_message(request, messages.SUCCESS, 
                                     f'Complain for {full_name} was successfully editted.')
            
            return HttpResponseRedirect(reverse('edit_complain', args=[pk]))
        context = {"user_edit": complain}  
        return render(request, 'Trackerfolder/edit_complain.html', context)
        
    except Exception as e:
        messages.add_message(request, messages.WARNING,
                             'An error occurred while edit user complain.')
        return HttpResponseRedirect(reverse('edit_complain', args=[pk]))

def pend_jobs(request):
    
    return render(request, 'Trackerfolder/pend_jobs.html')


def pend_payments(request):
    
    return render(request, 'Trackerfolder/pend_payments.html')
