from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
from datetime import datetime
import bcrypt

def show_login(request):
    if request.method == "GET":
        print("*"*25 + "show_login" + "*"*25)
        print("In: show_login -> rendering index.html")
        return render(request, 'log_reg_app/index.html')

def process_login(request):
    # print("*"*25 + "process_login" + "*"*25)
    # print("In: process_login, Processinf login validation -> show_success")
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        errors = User.objects.login_validator(request.POST)
        context = { 'email': email, 'password': password }
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/", context)
        else:
            # There could be multiple instances of the desired email address
            users = User.objects.filter(email=email) # .password
            for user in users:
                passwd = user.password
                if bcrypt.checkpw(request.POST['password'].encode(), passwd.encode()):
                    request.session['user_id'] = user.id
                    return redirect("/success")
            try:
                del request.session['user_id']
            except KeyError:
                pass
            return redirect("/", context)

def process_registration(request):
    # print("*"*25 + "process_registration" + "*"*25)
    # print("In: process_registration, Processing registration -> show_success")
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST['last_name']
        email = request.POST['email']
        birthday = request.POST['birthday']
        password = request.POST['password']
        # confirm_pw = request.POST['confirm_pw'] # This line may not be needed
        errors = User.objects.registration_validator(request.POST)
        context = { 'first_name': first_name, 'last_name': last_name, 'email': email, 'birthday': birthday}
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/", context)
        else:
            hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hash1, birthday=birthday )
            request.session['user_id'] = user.id
            return redirect("/success", context)

def show_success(request):
    # print("*"*25 + "show_success" + "*"*25)
    # print("In: show_success -> render success.html")
    try:
        user_id = request.session['user_id']
    except KeyError:
        return redirect("/")
    user = User.objects.get(id=user_id)
    first_name = user.first_name
    #context = {'first_name': first_name, 'last_name': user.last_name, 'user_id': user.id }
    return redirect('/wall') # This is redirecting to the_wall_app 
    # return render(request, 'log_reg_app/success.html', context)

def log_out(request):
    # print("*"*25 + "log_out" + "*"*25)
    # print("In: log_out -> show_login")
    request.session.clear()
    return redirect("/")
