
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import os

def validate_file_access(path):
    """
    Path must exists 
    Path mus be a file
    Path must be readable
    """
    if not os.path.exists(path):
        raise ValidationError(_("Path Does Not Exist"))
    if not os.path.isfile(path):
        raise ValidationError(_("Path Is Not A Directory"))
    if not os.access(path, os.R_OK):
        raise ValidationError(_("Read Permission Denied"))

def validate_path_access(value):
    """
    Path must exists 
    Path mus be a Directory
    Path must be readable
    """
    if not os.path.exists(value):
        raise ValidationError(_("Path Does Not Exist"))
    if not os.path.isdir(value):
        raise ValidationError(_("Path Is Not A Directory"))
    if not os.access(value, os.R_OK):
        raise ValidationError(_("Read Permission Denied"))