import csv, io
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from .models import AddComponent
from .forms import CreateDemandForm, CreateSolarForm, CreateBatteryForm, CreateGeneratorForm, CreateConverterForm, CreateControllerForm, CreateGridForm, AddComponentForm, AddToControllerForm

def index(request):
    components = AddComponent.objects.all()
    return render(request, 'optimizer/main.html', {'components': components})

def run_model(request):
    components = AddComponent.objects.all()
    return render(request, 'optimizer/main.html', {'components': components})

def add_component(request):
    components = AddComponent.objects.all()
    return render(request, 'optimizer/add_component.html', {'components': components})

def view_system(request):
    components = AddComponent.objects.all()
    return render(request, 'optimizer/view_system.html', {'components': components})

# All add component views
@permission_required('admin.can_add_log_entry')
def add_demand(request):
    components = AddComponent.objects.all()
    if request.method == "POST":
        create_form = CreateDemandForm(request.POST)
        add_form = AddComponentForm(request.POST)
        if create_form.is_valid() and add_form.is_valid():
            create = create_form.save()
            add = add_form.save(False)
            add.comp_type = 'demand'
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
            add = add_form.save(False)
            add.comp_type = 'battery'
            add.zone = 1
            add.save()

            create = create_form.save(False)
            create.component = add
            create.save()

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
            add = add_form.save(False)
            add.comp_type = 'solar'
            add.zone = 0
            add.save()

            create = create_form.save(False)
            create.component = add
            create.save()

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
            add = add_form.save(False)
            add.comp_type = 'converter'
            add.zone = 1
            add.save()

            create = create_form.save(False)
            create.component = add
            create.save()

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
            add = add_form.save(False)
            add.comp_type = 'generator'
            add.zone = 1
            add.save()

            create = create_form.save(False)
            create.component = add
            create.save()

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
            add = add_form.save(False)
            add.comp_type = 'grid'
            add.zone = 2
            add.save()

            create = create_form.save(False)
            create.component = add
            create.save()

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
            add = add_form.save(False)
            add.comp_type = 'controller'
            add.zone = 3
            add.save()

            create = create_form.save(False)
            create.component = add
            create.save()

            return redirect('add_component')
    else:
        create_form = CreateControllerForm()
        add_form = AddComponentForm()

    args = {}
    args['components'] = components
    args['create_form'] = create_form
    args['add_form'] = add_form
    return render(request, 'optimizer/add_controller.html', args)

# All view component views
def view_component(request, comp_name):
    components = AddComponent.objects.all()
    active_components = AddComponent.objects.filter(zone=1) # Find all active components
    input_component = AddComponent.objects.get(comp_name=comp_name)

    if request.method =="POST":
        return redirect('add_component')

    args = {}
    args['components'] = components
    args['input_component'] = input_component
    args['active_components'] = active_components
    args['comp_name']=comp_name
    return render(request, f'optimizer/view_{input_component.comp_type}.html', args)

def add_to_controller(request, comp_name, add_to_cont_name):
    components = AddComponent.objects.all()
    input_component = AddComponent.objects.get(comp_name=add_to_cont_name)

    if request.method == "POST":
        if input_component.comp_type=='battery':
            add_form = AddToControllerForm(request.POST)
        elif input_component.comp_type=='converter':
            converter = AddToController(component=AddComponent.input_component,
                                        mode='bidirectional',
                                        configs='{}')
            return redirect('view_component', comp_name=comp_name)
    else:
        add_form = AddToControllerForm()
