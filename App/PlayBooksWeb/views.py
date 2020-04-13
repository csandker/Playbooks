from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError
from requests.exceptions import MissingSchema
from django.contrib.auth.decorators import login_required

from PlayBooksWeb.models import IncludedFolder
from .forms import IncludeFolderForm 

@login_required
@csrf_protect
def includeFolderIndex(request):
    folders = IncludedFolder.objects.all()
    context = {
        'folders': folders
    }
    return render(request, '_folder_index.html', context)

@login_required
@csrf_protect
def includeFolderAdd(request):
    context = {
        'form': IncludeFolderForm()
    }
    ## POST REQ
    if( request.method == 'POST' ):
        form = IncludeFolderForm(request.POST)
        if( form.is_valid() ):
            ## all valid
            form.save()
            if( not request.POST.get('_addanother', False) ):
                return redirect('/admin/')
        else:
            ## Form not valid
            context['form'] = form 

    return render(request, 'folder_change.html', context)

@login_required
@csrf_protect
def includeFolderChange(request, folderID):
    folder = get_object_or_404(IncludedFolder, pk=folderID)
    context = {'folder': folder}
    context['form'] = IncludeFolderForm(instance=folder) 
    if( request.method == 'POST' ):
        form = IncludeFolderForm(request.POST, instance=folder)
        if( form.is_valid() ):
            form.save()
            return redirect('/admin/')
        
        else:
            context['form'] = form 
    
    return render(request, 'folder_change.html', context)
        
@login_required
@csrf_protect
def includeFolderDelete(request, folderID):
    folder = get_object_or_404(IncludedFolder, pk=folderID)
    folder.delete()
    
    return redirect('/admin/')
