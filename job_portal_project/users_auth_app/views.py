from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from users_auth_app.models import*
from employer_app.models import EmployerProfileModel
from candidate_app.models import CandidateProfileModel

# Create your views here.
# home_page
def home_page(request):
   
    return render(request, 'home_page.html')




# register
def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        user_type = request.POST.get('user_type')
        
        if user_type == 'admin':
            CustomUserModel.objects.create_user(
                username=username,
                password=phone,
                email=email,
                user_type=user_type,
            )
            return redirect('login_page')

        else:   
            PendingAcountModel.objects.create(
                username=username,
                phone=phone,
                email=email,
                user_type=user_type,
                pending_status='pending'
            )
            return redirect('login_page')
    return render(request, 'register.html')

# Login view

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')  

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home_page')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login_page')
      
    return render(request, 'login.html')

# Logout view
def logout_page(request):

    logout(request)
    return redirect('login_page')


# changepass
def chnge_pass(request):
    curnt_user = request.user

    if request.method == 'POST':
        current_password = request.POST.get("current_password")
        confirm_password = request.POST.get("confirm_password")
        new_password = request.POST.get("new_password")

        if check_password(current_password, request.user.password):
          
            if new_password == confirm_password:
                curnt_user.set_password(new_password)  
                curnt_user.save()
                update_session_auth_hash(request, curnt_user)
                return redirect("login_page")

    return render(request, "change_pass.html")

# panding list

def panding_list(request):
    pandingUser=PendingAcountModel.objects.all()

    context={
        'pandingUser': pandingUser,
    }

    return render(request,'panding_list.html',context)
# accept button
def acceptUser(request, id):
    if request.method == 'POST':
        panding_data=PendingAcountModel.objects.get(id=id)
        if panding_data:
            user_data=CustomUserModel.objects.create_user(
                username=panding_data.username,
                password=panding_data.phone,
                email=panding_data.email,
                user_type=panding_data.user_type,
            )
        if user_data:
            if panding_data.user_type == 'employer':
                EmployerProfileModel.objects.create(
                    employer_user=user_data,
                    phone=panding_data.phone,
                    email=panding_data.email,
                )
            elif panding_data.user_type == 'candidate':
                CandidateProfileModel.objects.create(
                    employer_user=user_data,
                    phone=panding_data.phone,
                    email=panding_data.email,
                )
        panding_data.delete()

    return redirect('panding_list')

def Reject(request,id):
    # if request.method =='POST':
    #     panding_data=PendingAcountModel.objects.get(id=id)
    #     if panding_data:
    #         panding_data.delete()
    return redirect('panding_list')



