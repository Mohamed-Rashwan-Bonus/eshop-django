from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, EmailLoginForm


def register_view(request):
    """Req 1,2,3,4,5: registration page with validation."""
    if request.user.is_authenticated:
        return redirect('catalog:product_list')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(request, user)
        messages.success(request, f'Welcome {user.first_name}!')
        return redirect('catalog:product_list')
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Req 6: login with email + password."""
    if request.user.is_authenticated:
        return redirect('catalog:product_list')
    form = EmailLoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect(request.GET.get('next') or 'catalog:product_list')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Req 7."""
    logout(request)
    return redirect('catalog:product_list')


@login_required
def profile_view(request):
    """Req 8: profile after authentication."""
    return render(request, 'accounts/profile.html')
