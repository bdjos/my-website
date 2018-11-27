import csv, io
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from .models import CreateSolar, CreateBattery, AddBattery, AddComponent
from .forms import CreateSolarForm, CreateBatteryForm, AddBatteryForm, AddComponentForm

def index(request):
    components = AddCom ponent.objects.all()
    return render(request, 'optimizer/main.html', {'components': components})

def run_model(request):
    components = AddComponent.objects.all()
    return render(request, 'optimizer/main.html', {'components': components})

def add_component(request):
    components = AddComponent.objects.all()
    return render(request, 'optimizer/add_component.html', {'components': components})

@permission_required('admin.can_add_log_entry')
def add_demand(request):
    components = AddComponent.objects.all()
    if request.method == "POST":
        create_form = CreateDemandForm(request.POST)
        add_form = AddComponentForm(request.POST)
        if create_form.is_valid() and add_form.is_valid():
            create = create_form.save()
            add = add_form.save(False)
            add.comp_type = 'Demand'
            add.object_id = 1
            add.createcomponent = create
            add.save()
            return redirect('add_component')
    else:
        create_form = CreateDemandForm()
        add_form = AddComponentForm()

    args = {}
    args['components'] = components
    args['create_form'] = create_form
    args['add_form'] = add_form
    return render(request, 'optimizer/add_demand.html', args)

def add_battery(request):
    components = AddComponent.objects.all()
    if request.method == "POST":
        create_form = CreateBatteryForm(request.POST)
        add_form = AddComponentForm(request.POST)
        if create_form.is_valid() and add_form.is_valid():
            create = create_form.save()
            add = add_form.save(False)
            add.comp_type = 'Battery'
            add.object_id = 1
            add.createcomponent = create
            add.save()
            return redirect('add_component')
    else:
        create_form = CreateBatteryForm()
        add_form = AddComponentForm()

    args = {}
    args['components'] = components
    args['create_form'] = create_form
    args['add_form'] = add_form
    return render(request, 'optimizer/add_battery.html', args)

def add_solar(request):
    components = AddComponent.objects.all()
    if request.method == "POST":
        create_form = CreateSolarForm(request.POST)
        add_form = AddComponentForm(request.POST)
        if create_form.is_valid() and add_form.is_valid():
            create = create_form.save()
            add = add_form.save(False)
            add.comp_type = 'Solar'
            add.object_id = 1
            add.createcomponent = create
            add.save()
            return redirect('add_component')
    else:
        create_form = CreateSolarForm()
        add_form = AddComponentForm()

    args = {}
    args['components'] = components
    args['create_form'] = create_form
    args['add_form'] = add_form
    return render(request, 'optimizer/add_solar.html', args)

def add_converter(request):
    components = AddComponent.objects.all()
    if request.method == "POST":
        create_form = CreateConverterForm(request.POST)
        add_form = AddComponentForm(request.POST)
        if create_form.is_valid() and add_form.is_valid():
            create = create_form.save()
            add = add_form.save(False)
            add.comp_type = 'Converter'
            add.object_id = 1
            add.createcomponent = create
            add.save()
            return redirect('add_component')
    else:
        create_form = CreateConverterForm()
        add_form = AddComponentForm()

    args = {}
    args['components'] = components
    args['create_form'] = create_form
    args['add_form'] = add_form
    return render(request, 'optimizer/add_converter.html', args)

def add_generator(request):
    components = AddComponent.objects.all()
    if request.method == "POST":
        create_form = CreateGeneratorForm(request.POST)
        add_form = AddComponentForm(request.POST)
        if create_form.is_valid() and add_form.is_valid():
            create = create_form.save()
            add = add_form.save(False)
            add.comp_type = 'Generator'
            add.object_id = 1
            add.createcomponent = create
            add.save()
            return redirect('add_component')
    else:
        create_form = CreateGeneratorForm()
        add_form = AddComponentForm()

    args = {}
    args['components'] = components
    args['create_form'] = create_form
    args['add_form'] = add_form
    return render(request, 'optimizer/add_generator.html', args)

def add_grid(request):
    components = AddComponent.objects.all()
    if request.method == "POST":
        create_form = CreateGridForm(request.POST)
        add_form = AddComponentForm(request.POST)
        if create_form.is_valid() and add_form.is_valid():
            create = create_form.save()
            add = add_form.save(False)
            add.comp_type = 'Grid'
            add.object_id = 1
            add.createcomponent = create
            add.save()
            return redirect('add_component')
    else:
        create_form = CreateGridForm()
        add_form = AddComponentForm()

    args = {}
    args['components'] = components
    args['create_form'] = create_form
    args['add_form'] = add_form
    return render(request, 'optimizer/add_grid.html', args)

def add_controller(request):
    components = AddComponent.objects.all()
    if request.method == "POST":
        create_form = CreateControllerForm(request.POST)
        add_form = AddComponentForm(request.POST)
        if create_form.is_valid() and add_form.is_valid():
            create = create_form.save()
            add = add_form.save(False)
            add.comp_type = 'Controller'
            add.object_id = 1
            add.createcomponent = create
            add.save()
            return redirect('add_component')
    else:
        create_form = CreateControllerForm()
        add_form = AddComponentForm()

    args = {}
    args['components'] = components
    args['create_form'] = create_form
    args['add_form'] = add_form
    return render(request, 'optimizer/add_controller.html', args)
