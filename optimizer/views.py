from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CreateBattery
from .forms import CreateBatteryForm

class header_pages():
    def __init__(self):
        self.components = CreateBattery.objects.all()

    @classmethod
    def index(cls, request):
        cls.__init__(cls)
        return render(request, 'optimizer/main.html', {'components': cls.components})

    @classmethod
    def run_model(cls, request):
        cls.__init__(cls)
        return render(request, 'optimizer/main.html', {'components': cls.components})

    @classmethod
    def add_component(cls, request):
        cls.__init__(cls)
        return render(request, 'optimizer/add_component.html', {'components': cls.components})

    @classmethod
    def add_demand(cls, request):
        cls.__init__(cls)
        return render(request, 'optimizer/add_demand.html', {'components': cls.components})

    @classmethod
    def add_battery(cls, request):
        cls.__init__(cls)
        if request.method == "POST":
            form = CreateBatteryForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
#                post.author = request.user
#                post.published_date = timezone.now()
                post.save()
                return redirect('add_component')
        else:
            form = CreateBatteryForm()
        return render(request, 'optimizer/add_battery.html', {'components': cls.components,'form': form})
