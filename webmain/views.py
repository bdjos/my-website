from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'webmain/home.html')

def ieso_predict(request):
    return render(request, 'webmain/ieso_predict.html')
