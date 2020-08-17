from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def register(request):
    new_user = UserCreationForm()
    if request.method == 'POST':
        new_user = UserCreationForm(request.POST)
        if new_user.is_valid():
            new_user.save()
            return redirect('/')
    return render(request, 'authentication/register_v1.html', {'form_register': new_user})