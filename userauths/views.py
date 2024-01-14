from django.shortcuts import render ,redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout

from userauths.models import User
from django.contrib import messages

def RegisterView(request):
    if request.method=="POST":
      form=UserRegisterForm(request.POST)
      if form.is_valid():
        #  form.save()
        new_user=form.save()
        username=form.cleaned_data.get("username")
        messages.success(request, f"Hey {username}, your account was created succesfully")
        new_user=authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
        login(request,new_user)
        return redirect("account:account")
    
    if request.user.is_authenticated:
       messages.warning(request, f"You are already logged in.")
       return redirect("core:index")
    
    else:
       form=UserRegisterForm()

    context={
        "form":form
      }
    return render(request, "userauths/sign-up.html",context)
     
def Loginview(request):
   if request.method=="POST":
      email=request.POST.get("email")
      password=request.POST.get("password")

      try:
         user=User.objects.get(email=email)
         user=authenticate(request, email=email, password=password)

         if user is not None:
            login(request, user)
            messages.success(request, "You are succesfully logged in.")
            return redirect("account:account")
         else:
            messages.warning(request, "Username or password does not exist")
            return redirect("userauths:sign-in")
      except:
         messages.warning(request, "User does not exist")

   if request.user.is_authenticated:
      messages.warning(request, "you are already logged In")
      return redirect("account:account")
        
   return render(request, "userauths/sign-in.html")

def LogoutView(request):
   logout(request)
   messages.success(request, "You have been logged out")
   return redirect("userauths:sign-in")
      