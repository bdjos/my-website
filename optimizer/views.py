from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'optimizer/main.html')

def add_component(request):
    return render(request, 'optimizer/add_component.html')

def add_demand(request):
    return render(request, 'optimizer/add_demand.html')
