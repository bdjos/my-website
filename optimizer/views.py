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
from .models import AddComponent, CreateDemand, CreateSystem, ComponentOutputs
from .forms import CreateSystemForm, CreateDemandForm, CreateSolarForm, CreateBatteryForm, CreateGeneratorForm, CreateConverterForm, CreateControllerForm, CreateGridForm, AddToControllerForm

def index(request):
    components = AddComponent.objects.all()
    return render(request, 'optimizer/main.html', {'components': components})

def run_model(request, sys_id):
    system = CreateSystem.objects.get(pk=sys_id)
    components = AddComponent.objects.filter(system_name=system)
    args = {}
    args['sys_id'] = sys_id
    args['system_name'] = system.system_name
    args['components'] = components
    return render(request, 'optimizer/add_component.html', args)

def add_component(request, sys_id):
    system = CreateSystem.objects.get(pk=sys_id)
    components = AddComponent.objects.filter(system_name=system)
    args = {}
    args['sys_id'] = sys_id
    args['system_name'] = system.system_name
    args['components'] = components
    return render(request, 'optimizer/add_component.html', args)

def view_system(request, sys_id):
    system = CreateSystem.objects.get(pk=sys_id)
    components = AddComponent.objects.filter(system_name=system)
    args = {}
    args['sys_id'] = sys_id
    args['system_name'] = system.system_name
    args['components'] = components
    return render(request, 'optimizer/view_system.html', args)

def create_system(request):
    if request.method == "POST":
        create_form = CreateSystemForm(request.POST)
        if create_form.is_valid():
            create = create_form.save()
            create.sys_id=create.pk
            return redirect('add_component', sys_id=create.sys_id)
    else:
        create_form = CreateSystemForm()

    args ={}
    args['create_form'] = create_form
    return render(request, 'optimizer/create_system.html', args)

### Add Component Defs
def sys_info(sys_id, comp_type):
    "Returns all the system info and html args for each component. Use in add_component views"
    system = CreateSystem.objects.get(pk=sys_id)
    components = AddComponent.objects.filter(system_name=system)
    of_type = AddComponent.objects.filter(system_name=system, comp_type=comp_type)
    comp_num=len(of_type) + 1
    comp_name = comp_type[:3] + str(comp_num)

    args = {}
    args['sys_id'] = sys_id
    args['system_name'] = system.system_name
    args['components'] = components
    return system, components, of_type, comp_num, comp_name, args

class return_errors():
    @classmethod
    def single_component(cls, comp_type):
        return f"""
                Only one {comp_type} allowed per system. To change {comp_type}, delete
                component by selecting it from the system view in the sidebar and add
                a new {comp_type}.
                """

def add_system_component(request, sys_id, comp_type):
    comp_type = comp_type
    system, components, of_type, comp_num, comp_name, args = sys_info(sys_id, comp_type)
    comp_data =  {
                'demand': {'form': CreateDemandForm, 'single_comp': 1, 'zone': 0},
                'battery': {'form': CreateBatteryForm, 'single_comp': 0, 'zone':1},
                'solar': {'form': CreateSolarForm, 'single_comp': 1, 'zone': 0},
                'generator': {'form': CreateGeneratorForm, 'single_comp': 1, 'zone': 1},
                'converter': {'form': CreateConverterForm, 'single_comp': 1, 'zone': 1},
                'controller': {'form': CreateControllerForm, 'single_comp': 1, 'zone': 1},
                'grid': {'form': CreateGridForm, 'single_comp': 1, 'zone': 2},
                }
    return_error = None

    if request.method == "POST":
        create_form = comp_data[comp_type]['form'](request.POST, request.FILES)
        if create_form.is_valid():
            add = AddComponent(system_name=system, comp_name=comp_name, comp_type=comp_type, comp_num=comp_num, zone=zone)
            add.save()

            create = create_form.save(False)
            create.component = add
            create.save()

            return redirect('add_component', sys_id)
    else:
        if comp_num > 1 & comp_data[comp_type]['single_comp']==1:
            return_error = return_errors.single_component(comp_type)
        else:
            return_error = None
        create_form = comp_data[comp_type]['form']()

    args['return_error'] = return_error
    args['create_form'] = create_form

    return render(request, f'optimizer/add_{comp_type}.html', args)

# All view component views
def view_component(request, sys_id, comp_name):
    system = CreateSystem.objects.get(pk=sys_id)
    components = AddComponent.objects.filter(system_name=system)
    active_components = AddComponent.objects.filter(system_name=system, zone=1) # Find all active components
    input_component = AddComponent.objects.get(system_name=system, comp_name=comp_name)

    if request.method =="POST":
        return redirect('add_component')

    args = {}
    args['sys_id'] = sys_id
    args['system_name'] = system.system_name
    args['components'] = components
    args['input_component'] = input_component
    args['active_components'] = active_components
    args['comp_name']=comp_name
    return render(request, f'optimizer/view_{input_component.comp_type}.html', args)

def add_to_controller(request, sys_id, controller, add_to_cont_name):
    system = CreateSystem.objects.get(pk=sys_id)
    components = AddComponent.objects.filter(system_name=system)
    input_component = AddComponent.objects.get(comp_name=add_to_cont_name)

    #
    if request.method == "POST":
        if input_component.comp_type=='battery':
            add_form = AddToControllerForm(request.POST)
            if add_form.is_valid():
                add = add_form.save(False)
                add.component = input_component
                add.save()
                return redirect('view_component', sys_id=sys_id, comp_name=comp_name)

    else:
        ## Here add if statements for different types of components
        if input_component.comp_type=='battery':
            add_form = AddToControllerForm()
        elif input_component.comp_type=='converter':
            converter = AddToController(component=AddComponent.input_component,
                                        mode='ss')
            return redirect('view_component', sys_id=sys_id, comp_name=comp_name)
    #
    args = {}
    args['components'] = components
    args['controller'] = controller
    args['input_component'] = input_component
    args['add_form'] = add_form
    return render(request, 'optimizer/configure_controller.html', args)
    # return render(request, 'optimizer/configure_controller.html', args)

def view_demand(request, sys_id, comp_name):
    system = CreateSystem.objects.get(pk=sys_id)
    components = AddComponent.objects.filter(system_name=system)
    demand_obj = CreateDemand.objects.get(component=AddComponent.objects.get(system_name=system, comp_name=comp_name))
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
    args['sys_id'] = sys_id
    args['system_name'] = system.system_name
    args['input_component'] = comp_name
    args['components'] = components
    args['html'] = html
    return render(request, 'optimizer/view_demand.html', args)

def delete_component(request, sys_id, comp_name):
    system = CreateSystem.objects.get(pk=sys_id)
    AddComponent.objects.filter(system_name=system, comp_name=comp_name).delete()

    return redirect('index')
