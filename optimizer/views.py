import csv, io
import os
import sys
sys.path.insert(0, os.path.join('..', 'pv-optimizer'))
from mgridoptimizer.modules import mgrid_model
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from .models import AddComponent, CreateDemand
from .forms import CreateSystemForm, CreateDemandForm, CreateSolarForm, CreateBatteryForm, CreateGeneratorForm, CreateConverterForm, CreateControllerForm, CreateGridForm, AddComponentForm, AddToControllerForm

def common_args(sys_id):
    components = AddComponent.objects.all()
    args = {}
    args['sys_id'] = sys_id
    args['components'] = components

def index(request):
    components = AddComponent.objects.all()
    return render(request, 'optimizer/main.html', {'components': components})

def run_model(request):
    components = AddComponent.objects.all()
    return render(request, 'optimizer/main.html', {'components': components})

def add_component(request, sys_id):
    args = comon_args(sys_id)
    return render(request, 'optimizer/add_component.html', args)

def view_system(request):
    components = AddComponent.objects.all()
    return render(request, 'optimizer/view_system.html', {'components': components})

def create_system(request):
    components = AddComponent.objects.all()
    if request.method == "POST":
        create_form = CreateSystemForm(request.POST)
        if create_form.is_valid():
            create = create_form.save()
            return redirect('add_component')
    else:
        create_form = CreateSystemForm()

    args = {}
    args['components'] = components
    args['create_form'] = create_form
    return render(request, 'optimizer/create_system.html', args)

# All add component views
def add_demand(request):
    components = AddComponent.objects.all()
    if request.method == "POST":
        create_form = CreateDemandForm(request.POST, request.FILES)
        add_form = AddComponentForm(request.POST)
        if create_form.is_valid() and add_form.is_valid():
            add = add_form.save(False)
            add.system_name = CreateSystem.objects.get()
            add.comp_type = 'demand'
            add.zone = 2
            add.save()

            create = create_form.save(False)
            create.component = add
            create.save()

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
            solar_model = mgrid_model.solar.run_api(create.system_capacity, create.base_cost, create.perw_cost)
            data = str(solar_model.json_demand)
            ComponentOutputs(component=add, output=data)
            create.save()

            return redirect('index')
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

def add_to_controller(request, controller, add_to_cont_name):

    components = AddComponent.objects.all()
    input_component = AddComponent.objects.get(comp_name=add_to_cont_name)

    #
    if request.method == "POST":
        if input_component.comp_type=='battery':
            add_form = AddToControllerForm(request.POST)
            if add_form.is_valid():
                add = add_form.save(False)
                add.component = input_component
                add.save()
                return redirect('view_component', comp_name=comp_name)

    else:
        ## Here add if statements for different types of components
        if input_component.comp_type=='battery':
            add_form = AddToControllerForm()
        elif input_component.comp_type=='converter':
            converter = AddToController(component=AddComponent.input_component,
                                        mode='ss')
            return redirect('view_component', comp_name=comp_name)
    #
    args = {}
    args['components'] = components
    args['controller'] = controller
    args['input_component'] = input_component
    args['add_form'] = add_form
    return render(request, 'optimizer/configure_controller.html', args)
    # return render(request, 'optimizer/configure_controller.html', args)

def view_demand(request, comp_name):
    components = AddComponent.objects.all()
    demand_obj = CreateDemand.objects.get(component=AddComponent.objects.get(comp_name=comp_name))
    path = os.path.join('media', str(demand_obj.demand))

    y =[]
    with open(path, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for val in reader:
            y.append(val[0])

    x = list(range(len(y)))
    figure_or_data = [go.Scatter({'x':x, 'y':y})]

    html = plotly.offline.plot(figure_or_data, include_plotlyjs=False, output_type='div')

    args = {}
    args['input_component'] = comp_name
    args['components'] = components
    args['html'] = html
    return render(request, 'optimizer/view_demand.html', args)

def delete_component(request, comp_name):
    AddComponent.objects.filter(comp_name=comp_name).delete()

    return redirect('index')
