from django.shortcuts import render, HttpResponse, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Welcome {username} your account has been succesfully created.")
            return redirect('users:login')
        
    form=RegisterForm()       
    context={
        'form':form
    }
    return render(request, 'users/register.html',context)

def logout_veiw(request):
    logout(request)
    return render(request, 'users/logout.html')

@login_required   
def profile(request):
    return render(request, 'users/profile.html')