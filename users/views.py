from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('sign_in')
    form = UserCreationForm()
    context = {'form': form}
    return render(request, 'sign_up.html', context)


def sign_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('article_func')
    form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'sign_in.html', context)


def sign_out(request):
    logout(request)
    return redirect('sign_in')
