from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

from store.forms import CustomUserForm

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User registration successful')
            return redirect('/login')
    context = {'form': form}
    return render(request, 'store/auth/register.html',context=context)

def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request, 'you are already logged in')
        return redirect('home')
    
    if request.method == 'POST':
        name = request.POST.get('username')
        pswd = request.POST.get('password')
        
        user  = authenticate(request,username=name, password=pswd)
        
        if user is not None:
            login(request,user)
            print("Successfully logged in")
            messages.success(request,"Login Successfully")
            return redirect('home')
        else:
            messages.error(request,"Invalid username or password")
            return redirect('/login')
    return render(request, 'store/auth/login.html',{'title':'Login'})

def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logout Successfully")
    return redirect('home')