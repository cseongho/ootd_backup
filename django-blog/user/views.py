from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from blog.views import get_category_count
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.


def login_page(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('home')
        else:
            messages.error(request, '아이디 또는 비밀번호가 일치하지 않습니다')
    context = {
        'title': 'Login',
        'most_recent': most_recent,
        'category_count': category_count,
    }
    return render(request, 'users/login.html', context)

def logout_page(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    logout(request)
    messages.success(request, 'Log Out 완료!')
    context = {
        'title': 'Logout',
        'most_recent': most_recent,
        'category_count': category_count,
    }
    return render(request, 'users/logout.html', context)

def register(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    if request.user.is_authenticated:
        return redirect('profile')
    elif request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user.save()
            messages.success(
                request, f'{username} 회원가입이 완료되었습니다!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
        'most_recent': most_recent,
        'category_count': category_count,
    }
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request, '프로필 수정이 완료되었습니다!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'most_recent': most_recent,
        'category_count': category_count,
    }
    return render(request, 'users/profile.html', context)
