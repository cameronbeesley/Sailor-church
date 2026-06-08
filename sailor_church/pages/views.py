from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout

# Create your views here.
def index(request):
    return render(request, 'pages/index.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('pages:index')
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('pages:index')
    return render(request, 'registration/logout.html')