from django.shortcuts import render
from pages.models import ConnectGroup

# Create your views here.
def index(request):
    return render(request, 'connect/index.html', {
        'groups': request.user.joined_groups.all()
    })

def join(request):
    return render(request, 'connect/join_page.html', {
        'available_groups': ConnectGroup.objects.all()
    })