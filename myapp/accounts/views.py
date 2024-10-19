# accounts/views.py
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import CustomUser 

def signup_view(request):
    form = CustomUserCreationForm()  # Default form initialization

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Reinitialize with POST data
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            return redirect('login')  # Ensure this URL name matches your URL patterns
        else:
            # Print form errors for debugging
            print("Form errors:", form.errors)  # Now this will always have a value

    return render(request, 'signup.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('admin_home') 
            return redirect('home')  # Adjust the redirect as per your URLs
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def home_view(request):
     if request.user.is_superuser:
        return redirect('admin_home')  # Redirect to admin home
     return render(request, 'home.html', {'user': request.user})
@login_required
def admin_home_view(request):
    users = CustomUser.objects.all()
    return render(request, 'admin_home.html', {'users': users, 'user': request.user})
@login_required
def create_user_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'create_user.html', {'form': form})
@login_required
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
@login_required
def delete_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        print(f"User with ID {user_id} deleted.") 
        return redirect('admin_home')
    return render(request, 'delete_user.html')
def logout_view(request):
    logout(request)
    return redirect('login')  # Adjust the redirect as per your URLs
