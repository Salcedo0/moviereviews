from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request ):
    # return render(request, 'index.html')
    return render(request, 'index.html', {'name': 'Juan Andres'})

def about(request):
    return render(request, 'about.html')