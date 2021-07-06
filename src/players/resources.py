from import_export import resources
from .models import Players

class PlayersResource(resources.ModelResource):
    class Meta:
        model = Players