from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CreateBattery, AddBattery
from .forms import CreateBatteryForm, AddBatteryForm

def index(request):
    components = AddBattery.objects.all()
    return render(request, 'optimizer/main.html', {'components': components})

def run_model(request):
    components = AddBattery.objects.all()
    return render(request, 'optimizer/main.html', {'components': components})

def add_component(request):
    components = AddBattery.objects.all()
    return render(request, 'optimizer/add_component.html', {'components': components})

def add_demand(request):
    components = AddBattery.objects.all()
    return render(request, 'optimizer/add_demand.html', {'components': components})

def add_battery(request):
    components = AddBattery.objects.all()
    if request.method == "POST":
        create_form = CreateBatteryForm(request.POST)
        add_form = AddBatteryForm(request.POST)
        if create_form.is_valid() and add_form.is_valid():
            create = create_form.save()
            add = add_form.save(False)
            add.createbattery = create
            add.save()
            return redirect('add_component')
    else:
        create_form = CreateBatteryForm()
        add_form = AddBatteryForm()

    args = {}
    args['components'] = components
    args['create_form'] = create_form
    args['add_form'] = add_form
    return render(request, 'optimizer/add_battery.html', args)
