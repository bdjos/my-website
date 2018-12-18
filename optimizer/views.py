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
from .models import *
from .forms import *

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

class ReturnErrors:
    @classmethod
    def single_component(cls, comp_type):
        return f"""
                Only one {comp_type} allowed per system. To change {comp_type}, delete
                component by selecting it from the system view in the sidebar and add
                a new {comp_type}.
                """

class CreateData:

    def __init__(self, sys_id, comp_type):
        self.sys_id = sys_id
        self.comp_type = comp_type
        self.system = CreateSystem.objects.get(pk=self.sys_id)
        self.comp_data = {
            'demand': {'single_comp': 1, 'zone': 0, 'create_data': self.demand_data},
            'battery': {'single_comp': 0, 'zone': 1, 'create_data': None},
            'solar': {'single_comp': 1, 'zone': 0, 'create_data': self.solar_data},
            'generator': {'single_comp': 1, 'zone': 1, 'create_data': None},
            'converter': {'single_comp': 1, 'zone': 1, 'create_data': None},
            'controller': {'single_comp': 1, 'zone': 1, 'create_data': None},
            'grid': {'single_comp': 1, 'zone': 2, 'create_data': None},
            }
        self.comp_single = self.comp_data[self.comp_type]['single_comp']
        self.components = AddComponent.objects.filter(system_name=self.system)
        self.of_type = AddComponent.objects.filter(system_name=self.system, comp_type=self.comp_type)
        self.comp_num=len(self.of_type) + 1
        self.comp_name = self.comp_type[:3] + str(self.comp_num)

    def get_args(self):
        """Returns all the system info and html args for each component. Use in add_component views"""
        args = {}
        args['sys_id'] = self.sys_id
        args['system_name'] = self.system.system_name
        args['components'] = self.components
        return args

    def demand_data(self):
        path = os.path.join('media', str(demand_obj.demand))
        y =[]
        with open(path, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for val in reader:
                y.append(val[0])
        return str(y)

    def solar_data(self, *args):
        system_capacity, base_cost, perw_cost = args
        solar_object = mgrid_model.solar.run_api(system_capacity, base_cost, perw_cost)
        return solar_object.json_demand


    def add_component(self):
        add = AddComponent(
                system_name=self.system,
                comp_name=self.comp_name,
                comp_type=self.comp_type,
                comp_num=self.comp_num,
                zone=self.comp_data[self.comp_type]['zone'])
        add.save()
        return add

def add_system_component(request, sys_id, comp_type):
    comp_data = CreateData(sys_id, comp_type)

    args = comp_data.get_args()
    return_error = None

    if request.method == "POST":
        create_form = create_component_form(comp_type)(request.POST, request.FILES)
        if create_form.is_valid():
            add = comp_data.add_component()

            create = create_form.save(False)
            create.component = add

            #Generate graph data if components are demand or solar
            if comp_type == 'demand':
                create.data = comp_data.gen_graph_data()
            elif comp_type == 'solar':
                create.data = comp_data.gen_solar_data(
                                                create.system_capacity,
                                                create.base_cost,
                                                create.perw_cost
                                                )
            create.save()
            return redirect('add_component', sys_id)

    else:
        if comp_data.comp_num > 1 & comp_data.comp_single==1:
            return_error = ReturnErrors.single_component(comp_type)
        else:
            return_error = None
        create_form = create_component_form(comp_type)()

    args['return_error'] = return_error
    args['create_form'] = create_form
    args['comp_type'] = comp_type

    return render(request, f'optimizer/add_system_component.html', args)

# All view component views
def view_component(request, sys_id, comp_name):
    system = CreateSystem.objects.get(pk=sys_id)
    components = AddComponent.objects.filter(system_name=system)
    active_components = AddComponent.objects.filter(system_name=system, zone=1)
    input_component = AddComponent.objects.get(system_name=system, comp_name=comp_name)
    input_component_type = input_component.comp_type
    # Get a dict of values for the component

    models = {
        'demand': CreateDemand,
        'battery': CreateBattery,
        'solar': CreateSolar,
        'generator': CreateGenerator,
        'converter': CreateConverter,
        'controller': CreateController,
        'grid': CreateGrid,
        }

    input_component_qryset = models[input_component_type].objects.filter(component__system_name=system, component__comp_name=comp_name)
    input_component_values = input_component_qryset.values()[0]
    qryset_list = []
    for key in input_component_qryset:
        qryset_list.append((key, input_component_values[key]))

    if request.method =="POST":
        return redirect('add_component')

    args = {}
    args['sys_id'] = sys_id
    args['system_name'] = system.system_name
    args['components'] = components
    args['input_component'] = input_component
    args['qryset_list'] = qryset_list
    args['active_components'] = active_components
    args['comp_name'] = comp_name
    args['comp_type'] = input_component_type.capitalize()
    return render(request, f'optimizer/view_component.html', args)

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
    comp = AddComponent.objects.get(system_name=system, comp_name=comp_name)
    demand_obj = CreateDemand.objects.get(component=AddComponent.objects.get(system_name=system, comp_name=comp_name))
    path = os.path.join('media', str(demand_obj.demand_file))

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
    args['comp_type'] = comp.comp_type.capitalize()
    args['components'] = components
    args['html'] = html
    return render(request, 'optimizer/view_demand.html', args)

def delete_component(request, sys_id, comp_name):
    system = CreateSystem.objects.get(pk=sys_id)
    AddComponent.objects.filter(system_name=system, comp_name=comp_name).delete()

    return redirect('add_component', sys_id=sys_id)
