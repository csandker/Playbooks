from django.db import models
from django.core.exceptions import ValidationError

from .validators import validate_path_access, validate_file_access

import os
import re
import base64

class IncludedFolder(models.Model):
    name = models.CharField(max_length=500)
    path = models.CharField(max_length=10000, validators=[validate_path_access])
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    @classmethod
    def list_allowed_files(self, folderID, allowedExtensions):
        folder = self.objects.get( pk=folderID )
        path = folder.path
        allowedExtensionsTuple = ()
        ## Include Uppercases
        for ext in allowedExtensions:
            allowedExtensionsTuple += (ext,)
            allowedExtensionsTuple += (ext.upper(),)

        ## add trailing /
        path += '/' if path.endswith('') else ''
        ## create dict of files in folders
        global_dict = {}
        for file_root_path, dirs, files in os.walk(path):
            for file in files:
                if( file.endswith( allowedExtensionsTuple ) ):
                    ## cut off root path
                    containing_dir = file_root_path.replace(path, '')
                    containing_dir += '' if containing_dir.endswith('/') else '/'
                    files_array = []
                    if( containing_dir in global_dict ):
                        files_array = global_dict[containing_dir]
                    else:
                        global_dict[containing_dir] = files_array
                    file_option_value = "%s%s" %(containing_dir, file)
                    file_dict = { file_option_value: file }
                    files_array.append( file_dict )
                    global_dict[containing_dir] = files_array
                    
        global_options = self.dict_to_option_tuple(global_dict)
        return global_options
    
    @classmethod
    def dict_to_option_tuple(self, global_dict):
        dir_options = ()
        for folder_name in global_dict:
            folder_option = (folder_name,)
            fileoptions = ()
            files = global_dict[folder_name]
            for file_dict in files:
                for file_id in file_dict:
                    name = file_dict[file_id]
                    fileoption = (file_id, name)
                    fileoptions +=  ((fileoption),)
            
            
            folder_option += ((fileoptions),)
            dir_options += ( folder_option, ) 

        return ( dir_options )
    
    
    @classmethod
    def get_img_full_path(self, imgSubPath, folderID=None, subpath=None):
        folder = self.objects.get( pk=folderID )
        folder_path = folder.path
        folder_path += '' if folder_path.endswith('/') else '/'
        
        imgFullPath = os.path.abspath(os.path.join(folder_path, subpath, '..', imgSubPath))
        return imgFullPath

    @classmethod
    def valid_file_path(self, path):
        try:
            validate_file_access(path)
        except:
            return False
        else:
            return True
    
    @classmethod
    def path_validation(self, imgSubPath, folderID=None, subpath=None):
        imgFullPath =  self.get_img_full_path(imgSubPath, folderID=folderID, subpath=subpath)
        return self.valid_file_path(imgFullPath)
        
    @classmethod
    def path_processing(self, imgSubPath, folderID=None, subpath=None):
        imgFullPath =  self.get_img_full_path(imgSubPath, folderID=folderID, subpath=subpath)
        fdImg = os.open(imgFullPath, os.O_RDONLY)
        bufferImg = os.read(fdImg, os.path.getsize(fdImg))
        base64Img = base64.b64encode(bufferImg).decode('ascii')
        os.close(fdImg)

        if( base64Img ):
            return base64Img
        else:
            return False

    @classmethod
    def get_file_content(self, folderID, subpath):
        folder = self.objects.get( pk=folderID )
        path = folder.path
        path += '' if path.endswith('/') else '/'
        fullpath = '%s%s' %(path, subpath)
        fd = os.open(fullpath, os.O_RDONLY)
        buffer = os.read(fd, os.path.getsize(fd))
        content = buffer.decode('utf-8', errors='ignore')
        os.close(fd)
        
        return content
