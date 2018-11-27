from import_export import resources
from .models import CreateDemand

class DemandResource(resources.ModelResource):
    class Meta:
        model = CreateDemand
