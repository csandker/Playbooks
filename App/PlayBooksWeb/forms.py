from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .validators import validate_path_access
from .models import IncludedFolder

class IncludeFolderForm(ModelForm):
    class Meta:
        model = IncludedFolder
        fields = ['name', 'path', 'enabled']
        help_texts = {
            'name': _("Name of the folder. Can contain charachters, numbers, '-'' & '_'."),
            'path': _("Absolute Path. Access to it will be validated automatically"),
            'enabled': _("Path can be enabled and disabled dynamically"),
        }
        widgets={'path': forms.TextInput(attrs={'size': '80'})}
    