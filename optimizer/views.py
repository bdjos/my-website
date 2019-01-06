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
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
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

# Add Component Defs


class ReturnErrors:
    @classmethod
    def single_component(cls, comp_type):
        return f"""
                Only one {comp_type} allowed per system. To change {comp_type}, delete
                component by selecting it from the system view in the sidebar and add
                a new {comp_type}.
                """


class CreateData:
    """
    Abstracts the system component characteristics for the add_system_component view
    """

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
            'controller': {'single_comp': 1, 'zone': 2, 'create_data': None},
            'grid': {'single_comp': 1, 'zone': 3, 'create_data': None},
            }
        self.comp_single = self.comp_data[self.comp_type]['single_comp']
        self.comp_zone = self.comp_data[self.comp_type]['zone']
        self.components = AddComponent.objects.filter(system_name=self.system)
        self.of_type = AddComponent.objects.filter(system_name=self.system, comp_type=self.comp_type)
        self.comp_num = len(self.of_type) + 1
        self.comp_name = self.get_comp_name(self.comp_type, str(self.comp_num))

    @staticmethod
    def get_comp_name(comp_type, comp_num):
        vowels = ['a', 'e', 'i', 'o', 'u']
        for letter in comp_type:
            if letter in vowels:
                comp_type = comp_type.replace(letter, '')

        return (comp_type[:3] + comp_num)

    def get_args(self):
        """Returns all the system info and html args for each component. Use in add_component views"""
        args = {}
        args['sys_id'] = self.sys_id
        args['system_name'] = self.system.system_name
        args['components'] = self.components
        return args

    def demand_data(self, demand_file):
        path = os.path.join('media', str(demand_file))
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
                zone=self.comp_data[self.comp_type]['zone']
        )
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

            create = create_form.save(False) # Create Component object
            create.component = add
            create.save()

            # Generate graph data if components are demand or solar
            if comp_type == 'demand':
                create.data = comp_data.demand_data(create.demand_file)
            elif comp_type == 'solar':
                create.data = comp_data.solar_data(
                                                create.system_capacity,
                                                create.base_cost,
                                                create.perw_cost
                                                )
            create.save()

            # Add to controller table if components are in zone 1
            if add.zone == 1:
                add_controller_object = AddToController(component=add, mode='nc')
                add_controller_object.save()

            return redirect('add_component', sys_id)

    else:
        if comp_data.comp_num > 1 & comp_data.comp_single == 1:
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

    model_info = {
        'demand': {
            'model': CreateDemand,
            'spec_fields': []},
        'battery': {
            'model': CreateBattery,
            'spec_fields': [
                'energy_capacity',
                'soc_min',
                'soc_max',
                'base_cost',
                'energy_cost'
            ]
        },
        'solar': {
            'model': CreateSolar,
            'spec_fields': [
                'system_capacity',
                'base_cost',
                'perw_cost'
            ]
        },
        'generator': {
            'model': CreateGenerator,
            'spec_fields': [
                'power',
                'base_cost',
                'fuel_cost'
            ]
        },
        'converter': {
            'model': CreateConverter,
            'spec_fields': [
                'power',
                'base_cost',
                'power_cost',
            ]
        },
        'controller': {
            'model': CreateController,
            'spec_fields': []},
        'grid': {
            'model': CreateGrid,
            'spec_fields': [
                'energy_cost',
                'nm_allowed'
            ]
        }
    }

    # Get all component specs for displaying in view
    input_component_qryset = model_info[input_component_type]['model'].objects.filter(
        component__system_name=system,
        component__comp_name=comp_name
    )
    input_component_values = input_component_qryset.values()[0]
    qryset_list = []

    for key in input_component_values:
        if key in model_info[input_component_type]['spec_fields']:
            qryset_list.append((key, input_component_values[key]))

    # If demand or solar generate graph data
    html = None # Blank html for non solar or demand objects
    if input_component_type == 'demand' or input_component_type == 'solar':
        y = model_info[input_component_type]['model'].objects.get(
            component__system_name=system,
            component__comp_name=comp_name
        ).data
        y = y.split(',')

        x = list(range(len(y)))
        trace1 = go.Scatter({'x':x, 'y':y})
        data = [trace1]
        layout = go.Layout(
            xaxis=dict(
                title='Date',
                titlefont=dict(
                    size=18,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title='kW',
                titlefont=dict(
                    size=18,
                    color='#7f7f7f'
                )
            )
        )

        html = plotly.offline.plot({'data': data, 'layout': layout}, include_plotlyjs=False, output_type='div', link_text='')


    if request.method =="POST":
        return redirect('add_component', sys_id)

    args = {}
    args['sys_id'] = sys_id
    args['system_name'] = system.system_name
    args['components'] = components
    args['input_component'] = input_component
    args['qryset_list'] = qryset_list
    args['active_components'] = active_components
    args['comp_name'] = comp_name
    args['comp_type'] = input_component_type.capitalize()
    args['html'] = html
    return render(request, f'optimizer/view_component.html', args)

def configure_controller(request, sys_id, comp_name):
    system = CreateSystem.objects.get(pk=sys_id)
    components = AddComponent.objects.filter(system_name=system)
    controller_objects = AddComponent.objects.filter(system_name=system, zone=1)

    controller_not_configured = AddComponent.objects.filter(addtocontroller__configured="False")
    controller_configured = AddComponent.objects.filter(addtocontroller__configured="True")

    forms = []
    if request.method == "POST":
        for controller_object in controller_objects:
            form = AddToControllerForm(request.POST)
            if form.is_valid():
                create = form.save(False)
                create.component = controller_object
                create.configured = 'True'
                create.save()
            forms.append(AddToControllerForm(request.POST))
        return redirect('add_component', sys_id=sys_id)
    else:
        for controller_object in controller_objects:
            mode = controller_object.addtocontroller.mode
            forms.append(AddToControllerForm(initial={'mode': mode}))

    args = {
        'form': forms,
        'sys_id': sys_id,
        'system_name': system.system_name,
        'components': components,
        'controller': comp_name,
        'controller_objects': controller_objects,
        'controller_not_configured': controller_not_configured,
        'controller_configured': controller_configured}

    return render(request, 'optimizer/configure_controller_opt.html', args)

def add_to_controller(request, sys_id, controller, add_to_cont_name):
    system = CreateSystem.objects.get(pk=sys_id)
    components = AddComponent.objects.filter(system_name=system)
    input_component = AddComponent.objects.get(comp_name=add_to_cont_name)

    if request.method == "POST":
        if input_component.comp_type == 'battery':
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


def delete_component(request, sys_id, comp_name):
    system = CreateSystem.objects.get(pk=sys_id)
    AddComponent.objects.filter(system_name=system, comp_name=comp_name).delete()

    return redirect('add_component', sys_id=sys_id)
