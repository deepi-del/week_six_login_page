
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import CustomUser 
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control


def signup_view(request):
    #  away from the signup page
    if request.user.is_authenticated:
        return redirect('home' if not request.user.is_superuser else 'admin_home')

    #  form 
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home' if not user.is_superuser else 'admin_home')
    
    return render(request, 'signup.html', {'form': form})

@never_cache
def login_view(request):
    # Redirect already 
    if request.user.is_authenticated:
        return redirect('admin_home' if request.user.is_superuser else 'home')

    #  login form 
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        #  after login
        return redirect('admin_home' if user.is_superuser else 'home')
    
    return render(request, 'login.html', {'form': form})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
@login_required(login_url='login')

def home_view(request):
     if request.user.is_superuser:
        return redirect('admin_home')  
     return render(request, 'home.html', {'user': request.user})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
@login_required(login_url='login')
def admin_home_view(request):
    query = request.GET.get('q')  
    if query:
        users = CustomUser.objects.filter(username__icontains=query)  
    else:
        users = CustomUser.objects.all()  

    return render(request, 'admin_home.html', {'users': users, 'user': request.user})

@never_cache 
def create_user_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'create_user.html', {'form': form})

@never_cache 
def update_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_home')
    else:
        form = CustomUserCreationForm(instance=user)
    return render(request, 'update_user.html', {'form': form, 'user': user})

@never_cache 
def delete_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        print(f"User with ID {user_id} deleted.") 
        return redirect('admin_home')
    return render(request, 'delete_user.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
@login_required(login_url='login')
def logout_view(request):
    logout(request)
    request.session.flush()  
    return redirect('login')
