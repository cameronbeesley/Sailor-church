from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'connect/index.html', {
        'groups': request.user.joined_groups.all()
    })