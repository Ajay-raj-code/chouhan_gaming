import datetime
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.contrib import auth
from django.contrib.auth.models import User
from .forms import UserForm
from django.contrib import messages
from .models import OTP
from django.contrib.auth.hashers import make_password
from django.utils import timezone

timezone.now() 
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        context = {"auth": True}
    else:
        context = {"auth": False}
    return render(request, "index.html", context=context)

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('login')
         
        # Authenticate the user with the provided username and password
        user = auth.authenticate(username=username, password=password)
         
        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect('login')
        else:
            login(request, user)
            return redirect("home")
    
    return render(request, "login.html")

def fun(u):
    me = "ajay.raj.635p@gmail.com"
    person = User.objects.get(username = u)
    name = person.first_name
    you = person.email

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Link"
    msg['From'] = "me@gmail.com"
    msg['To'] = you
    opt = random.randint(100000, 999999)
    g = OTP.objects.filter(user = person.id) or None
    if g is None:
        x = OTP()
        x.user = person
        x.otp = opt
        x.times = datetime.datetime.now()
        
    else:
        x = OTP.objects.get(user = person.id)

        x.otp = opt
        x.times = datetime.datetime.now()
    x.save()
    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    html = f"""
    <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <style>
                body{{font-size: 18px;}}
                #parent{{margin: auto;
                    width: 500px;
                    padding: 10px;   
                    height: 550px;}}
                .button-18 {{align-items: center;
                background-color: #0A66C2;
                border: 0;
                border-radius: 100px;
                box-sizing: border-box;
                color: #ffffff;
                cursor: pointer;
                display: inline-flex;
                font-family: -apple-system, system-ui, system-ui, "Segoe UI", Roboto, "Helvetica Neue", "Fira Sans", Ubuntu, Oxygen, "Oxygen Sans", Cantarell, "Droid Sans", "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Lucida Grande", Helvetica, Arial, sans-serif;
                font-size: 16px;
                font-weight: 600;
                justify-content: center;
                line-height: 20px;
                max-width: 480px;
                min-height: 40px;
                min-width: 0px;
                overflow: hidden;
                padding: 0px;
                padding-left: 20px;
                padding-right: 20px;
                text-align: center;
                touch-action: manipulation;
                transition: background-color 0.167s cubic-bezier(0.4, 0, 0.2, 1) 0s, box-shadow 0.167s cubic-bezier(0.4, 0, 0.2, 1) 0s, color 0.167s cubic-bezier(0.4, 0, 0.2, 1) 0s;
                user-select: none;
                -webkit-user-select: none;
                vertical-align: middle;}}
                
                .button-18:hover,
                .button-18:focus {{background-color: #16437E;
                color: #ffffff;}}
                
                .button-18:active {{background: #09223b;
                color: rgb(255, 255, 255, .7);}}
                
                .button-18:disabled {{cursor: not-allowed;
                background: rgba(0, 0, 0, .08);
                color: rgba(0, 0, 0, .3);}}
            
            </style>
        </head>
        <body>
            <div id="parent">
                <p>Hi,</p>
                <p>To procedd further with your registration process please enter the otp</p>
                
                <h1 style="text-align: center;">Dear {name}</h1>  
                <br>
                <p style="text-align: center;">Your email varification OTP is</p>
        
                <button onclick="copy()" class="button-18" role="button" style="margin-top: 0px; margin-left:auto;margin-right:auto;display:block;" id="otp">{opt}</button>

                <p style="text-align: center;">Please note that this OTP will only be valid for 180 seconds.</p>
                <br><br>
                <p style="text-align: center; color: darkviolet;">ajay.raj.635p@gmail.com</p>
                <p style="text-align: center; font-weight: bold; margin-bottom: 0px;">Cheers</p>
                <p style="text-align: center; margin-top: 0px;">About Chouhan Gaming</p>
                <script>
                    function copy()/{{
                        var copyText = document.getElementById("otp").innerText;
                        navigator.clipboard.writeText(copyText);
                    }}
                </script>
            </div>
        </body>
        </html>

    """

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login('ajay.raj.635p@gmail.com', 'itix povw zuts jtyy')
    mail.sendmail(me, you, msg.as_string())
    mail.quit()
    
def registerPage(request):
    
    if request.method == "POST":
        forms = UserForm(request.POST)
        forms.fields['username'].widget.attrs = {'class':'form-control','placeholder':'Username', 'name':'username'}
        forms.fields['first_name'].widget.attrs = {'class':'form-control','placeholder':'First Name', 'name':'first_name'}
        forms.fields['last_name'].widget.attrs = {'class':'form-control','placeholder':'Last Name', 'name':'last_name'}
        forms.fields['email'].widget.attrs = {'class':'form-control','placeholder':'Email', 'name': 'email'}
        forms.fields['password'].widget.attrs = {'class':'form-control','placeholder':'Password', 'name':'password'}
        u = request.POST.get("username")
        p = request.POST.get("password")
        if  User.objects.filter(username=u).exists():
            user = auth.authenticate(request, username=u, password=p)
            if user is not None:
                fun(u)
                return redirect("varify", users= u)
        if forms.is_valid():
            username = forms.cleaned_data.get('username')
            print("username")
            password = forms.cleaned_data["password"]
            email = forms.cleaned_data["email"]
            fname = forms.cleaned_data["first_name"]
            lname = forms.cleaned_data["last_name"]
            x= User(username = username, password = make_password(password), email = email, first_name = fname, last_name = lname)
            x.save()
            fun(username)
            return redirect("varify", users= username)
    
    else:
        forms = UserForm()
        forms.fields['username'].widget.attrs = {'class':'form-control','placeholder':'Username', 'name':'username'}
        forms.fields['first_name'].widget.attrs = {'class':'form-control','placeholder':'First Name', 'name':'first_name'}
        forms.fields['last_name'].widget.attrs = {'class':'form-control','placeholder':'Last Name', 'name':'last_name'}
        forms.fields['email'].widget.attrs = {'class':'form-control','placeholder':'Email', 'name': 'email'}
        forms.fields['password'].widget.attrs = {'class':'form-control','placeholder':'Password', 'name':'password'}
    
    context={
        "forms":forms
    }
    
    return render(request, "registration.html", context=context)

def varify(request, users):
    ua = User.objects.get(username = users)
    x= OTP.objects.get(user=ua.id)
    d1 = datetime.datetime.now().date() - x.times.date()
    t1 = datetime.datetime.now().time().minute -  x.times.time().minute
    h1 =datetime.datetime.now().time().hour -  x.times.time().hour


    if d1.days == 0 and h1 == 0 and t1<3:
        if request.method == "POST":
            otp = request.POST.get("otp")
            if otp == str(x.otp):
                return redirect("login")
            else:
                messages.info(request, f'Invalid OTP. Try again..')
        else:
            return render(request, "otp.html")
    else:
        return redirect("otp", users = users)
    

def logout(request):
    auth.logout(request)
    return redirect("home")
