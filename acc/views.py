from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "acc/index.html")

def userlogin(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        user = authenticate(username=un, password=up)
        if user:
            login(request, user)
            messages.success(request, "로그인을 성공했습니다")
            return redirect("acc:index")
        else:
            messages.error(request, "일치하는 계정이 존재하지 않습니다")
    return render(request, "acc/login.html")

def signup(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        uc = request.POST.get("ucomm")
        pi = request.FILES.get("upic")
        try:
            User.objects.create_user(username=un, password=up, comment=uc, pic=pi)
            return redirect("acc:login")
        except:
            pass
    return render(request, "acc/signup.html")

def userlogout(request):
    logout(request)
    return redirect("acc:index")

def profile(request):
    return render(request, "acc/profile.html")

def delete(request):
    if request.method == "POST":
        ck = request.POST.get("pwck")
        if check_password(ck, request.user.password):
            request.user.pic.delete()
            request.user.delete()
            return redirect("acc:index") 
        else:
            pass
            return redirect("acc:profile")

def update(request):
    if request.method == "POST":
        u = request.user
        up = request.POST.get("upass")
        ue = request.POST.get("umail")
        uc = request.POST.get("ucomm")
        pi = request.FILES.get("upic")
        if up:
            u.set_password(up)
        u.email = ue
        u.comment = uc
        if pi:
            u.pic.delete()
            u.pic = pi
        u.save()
        login(request, u)
        return redirect("acc:profile")    
    return render(request, "acc/update.html")