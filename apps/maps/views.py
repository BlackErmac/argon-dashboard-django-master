from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def show_map(request):
    return render(request , 'maps/map.html')
