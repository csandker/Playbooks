from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required

from PlayBooksApp.models import Playbook, PlaybookSection, SectionContent, Playpage
from .forms import PlaypageForm, TEXTPLaypageForm, PlaybookSectionForm, PlaybookAddPageForm, PlaybookForm

import copy
import json

from .request import URLRequester
from .markdown import MarkdownParser
from .source_resolver import SourceResolver


@login_required
@csrf_protect
def index(request):
    if( request.POST ):
        form = PlaybookForm(request.user, request.POST)
        if( form.is_valid() ):
            form.save()
            return redirect('index')
    else:
        form = PlaybookForm(request.user)
    
    playbooks = Playbook.user_all(request.user)
    context = {
        'playbooks': playbooks,
        'form': form
    }
    return render(request, 'index.html', context)

@login_required
@csrf_protect
def deletePlaybook(request, pbID):
    if( request.POST ):
        playbook = get_object_or_404(Playbook, pk=pbID)
        if( playbook.can_delete(request.user) ):
            for section in playbook.sections.all():
                deleteSection(request, section.id)
            playbook.delete()
        else:
            return HttpResponse(status=403)
    
    return redirect('index')

@login_required
@csrf_protect
def playbook(request, pbID):
    playbook = get_object_or_404(Playbook, pk=pbID)
    sections = playbook.user_sections(request.user)
    section_form = PlaybookSectionForm(request.user)
    context = {
        'playbook': playbook,
        'sections': sections,
        'section_form': section_form
    }


    return render(request, 'playbook.html', context)

@login_required
@csrf_protect
def editPage(request, pageID, sectionID):
    page = get_object_or_404(Playpage, pk=pageID)
    section = PlaybookSection.objects.get(pk=sectionID)
    form = PlaypageForm(request.user, instance=page)
    context = { 'page': page , 'form': form, 'section': section}

    return render(request, '_edit_page.html', context)

@login_required
@csrf_protect
def pageContent(request, pageID):
    page = get_object_or_404(Playpage, pk=pageID)
    if( page.can_access(request.user) ):
        ## make a deep copy, the real page object should not be changed
        page_copy = copy.deepcopy(page)
        if( request.POST ):
            ## EDIT page content
            form = TEXTPLaypageForm(request.user, request.POST, request.FILES, instance=page_copy, auto_id='textform_%s')
            ## Most effective way to clean form data
            if( form.is_valid() ):
                ## only update the offline store
                page.offline_store = form.instance.offline_store
                page.title = form.instance.title
                page.check_updates = form.instance.check_updates
                page.save()
            else:
                return HttpResponse(status=417)
        else:
            form = TEXTPLaypageForm(request.user, instance=page_copy, auto_id='textform_%s')
        
        parser = MarkdownParser()
        md_content = page.offline_store
        html_page = parser.parseMD(md_content) if md_content else ''

        context = {
            'form': form, 
            'html_page': html_page, 
            'page': page
        }

        return render(request, '_page_content.html', context)
    else:
        return HttpResponse( status=403 )

@login_required
@csrf_protect
def newPage(request, sectionID):
    section = PlaybookSection.objects.get(pk=sectionID)
    form = PlaypageForm(request.user)
    ## Only Add Existing Page Form if there are accessible pages
    add_page_form = False
    if( Playpage.accessible_pages(request.user) ):
        add_page_form = PlaybookAddPageForm(request.user)
    context = {
        'form': form,
        'add_page_form': add_page_form,
        'section': section 
    }
    
    return render(request, '_edit_page.html', context)

@login_required
@csrf_protect
def updatePage(request, pageID, sectionID):
    
    ## Only POST Requests
    playpage = get_object_or_404(Playpage, pk=pageID)
    if( playpage.can_access(request.user) ):
        if( request.POST ):
            form = PlaypageForm(request.user, request.POST, request.FILES, instance=playpage)
            if( form.is_valid() ):
                playpage = form.save()
            else:
                section = PlaybookSection.objects.get(pk=sectionID)
                context = { 'page': playpage , 'form': form, 'section': section}
                return render(request, '_edit_page.html', context, status=417)

        return HttpResponse( status=200 )
    else:
        return HttpResponse( status=403 )

@login_required
@csrf_exempt
def updatePagePosition(request, sectionID):
    if( request.is_ajax() ):
        try:
            data = json.loads(request.body)
            for dataset in data['positions']:
                position = dataset['position']
                pageID = dataset['page']
                page = get_object_or_404(Playpage, pk=pageID)
                if( page.can_change_position(request.user) ):
                    page.set_position(position, sectionID)
        except:
            return HttpResponse( status=500 )
        else:
            return HttpResponse( status=200 )

@login_required
@csrf_protect
def deletePage(request, sectionID, pageID):
    page = get_object_or_404(Playpage, pk=pageID)
    if( page.can_delete(request.user) ):
        try:
            ## if not existing in other sections delete page
            if ( page.sections.all().count() <= 1 ):
                page.delete()
                return HttpResponse( status=200 )
            else:
                ## Delete page only from section
                sectionContent = SectionContent.objects.filter(playpage=pageID, section=sectionID)
                sectionContent.delete()
                return HttpResponse( status=200 )
        except:
            return HttpResponse( status=500 )
    else:
        return HttpResponse( status=403 )

@login_required
@csrf_protect
def addPage(request, pbID, sectionID):
    form = PlaypageForm(request.user, request.POST, request.FILES)
    section = PlaybookSection.objects.prefetch_related().get(pk=sectionID)

    if( form.is_valid() ):
        ## all valid
        playpage = form.save()
        section.append_page(playpage)
    else:
        ## not valid form
        context = { 'form': form, 'section': section }
        return render(request, '_edit_page.html', context, status=417)

    return HttpResponse( status=200 )

@login_required
@csrf_protect
def addExistingPage(request, pbID, sectionID):
    section = get_object_or_404(PlaybookSection, pk=sectionID)
    form = PlaybookAddPageForm(request.user, request.POST, request.FILES)

    if( form.is_valid() ):
        ## get referenced page
        pageID = form['page'].data
        page = get_object_or_404(Playpage, pk=pageID)
        ## append page
        section.append_page( page )
        
    else:
        ## not valid form
        context = { 'form': form, 'section': section }
        return render(request, '_edit_page.html', context, status=417)

    return HttpResponse( status=200 )

@login_required
@csrf_protect
def addSection(request, pbID):
    playbook = get_object_or_404(Playbook, pk=pbID)
    section = PlaybookSection(playbook=playbook)
    form = PlaybookSectionForm(request.user, request.POST, instance=section)
    last_section = playbook.sections.last()
    if( last_section and last_section.section_position ):
        ## append to sections
        last_position = last_section.section_position
        section_position = last_position + 1
    else:
        ## No sections so far
        section_position = 0
    ## check valid
    if( form.is_valid() ):
        form.instance.section_position = section_position
        section = form.save()
        return HttpResponse( status=200 )
    else:
        return HttpResponse( status=417 )

@login_required
@csrf_protect
def deleteSection(request, sectionID):
    section = get_object_or_404(PlaybookSection, pk=sectionID)
    if( section.can_delete(request.user) ):
        section_pages = section.pages.all()
        ## check if pages exits on other sections
        for page in section_pages:
            ## if not existing in other sections delete page as well
            if ( page.sections.all().count() <= 1 ):
                if( page.can_delete(request.user) ):
                    page.delete()
        ## delete section
        section.delete()
        return HttpResponse( status=200 )
    else:
        return HttpResponse( status=403 )

@login_required
def apiServerFileOptions(request):
    if( request.POST['page_id'] ):
        pageID = request.POST.get('page_id')
        page = Playpage.objects.get( pk=pageID )
        if( page.can_access(request.user) ):
            form = PlaypageForm(request.user, request.POST, request.FILES, instance=page)
        else:
            return HttpResponse( status=403 )
    else:
        form = PlaypageForm(request.user, request.POST, request.FILES)
    
    form.is_valid() ## seems like the 'cleanest' option to call form.clean() 
    optgroups = form.get_included_folder_path_options()
    context = { 'optgroups':  optgroups }
    return render(request, '_select_server_file.html', context)

@login_required
def apiPrefetchSource(request):
    if( request.POST['page_id'] ):
        pageID = request.POST.get('page_id')
        page = Playpage.objects.get( pk=pageID )
        if( page.can_access(request.user) ):
            form = PlaypageForm(request.user, request.POST, request.FILES, instance=page)
        else:
            return HttpResponse( status=403 )
    else:
        form = PlaypageForm(request.user, request.POST, request.FILES)
    ## Clean form data
    source_type = form['source_type'].data
    valid_source = form.validate_source_type(source_type)
    
    if( valid_source ):
        form.is_valid() ## seems like the 'cleanest' option to call form.clean() 
        md_content = form.instance.offline_store
        parser = MarkdownParser()
        html = parser.parseMD( md_content )
        return HttpResponse( html, status=200 )
    else:
        return JsonResponse("Error", safe=False)

@login_required
def apiGetPageTitle(request, pageID):
    playpage = get_object_or_404(Playpage, pk=pageID)
    if( playpage.can_access(request.user) ):
        if( playpage ):
            page_title = playpage.title
            response = {'title': page_title}
            return JsonResponse( response, status=200 )
        else:
            response = {'title': ''}
            return JsonResponse( response, status=404 )
    else:
        return HttpResponse( status=403 )

@login_required
def apiPageUpateStatus(request, pageID):
    page = get_object_or_404(Playpage, pk=pageID)
    if( page.can_access(request.user) ):
        resolver = SourceResolver(page)
        updated_offline_store = resolver.resolve_type()
        if( updated_offline_store != page.offline_store ):
            return HttpResponse( status=200 )
        else:
            return HttpResponse( status=304 )
    else:
        return HttpResponse( status=403 )

@login_required
def apiUpdatePage(request, pageID):
    page = get_object_or_404(Playpage, pk=pageID)
    if( page.can_access(request.user) ):
        resolver = SourceResolver(page)
        updated_offline_store = resolver.resolve_type()
        if( updated_offline_store ):
            page.offline_store = updated_offline_store
            page.save()
            return HttpResponse( status=200 )
        else:
            return HttpResponse( status=500 )
    else:
        return HttpResponse( status=403 )

@login_required
def apiPrefetchUpdatePage(request, pageID):
    page = get_object_or_404(Playpage, pk=pageID)
    if( page.can_access(request.user) ):
        resolver = SourceResolver(page)
        updated_offline_store = resolver.resolve_type()
        if( updated_offline_store ):
            md_content = updated_offline_store
            parser = MarkdownParser()
            html = parser.parseMD( md_content )
            return HttpResponse( html, status=200 )
        else:
            return HttpResponse( status=500 )
    else:
        return HttpResponse( status=403 )

@login_required
def apiSearchPlaybooks(request):
    searchq = request.POST['search']
    results_all = Playpage.objects.filter(offline_store__contains=searchq)
    results_access = [ page for page in results_all if page.can_access(request.user) ]
    context = { 'pages': results_access }
    return render(request, '_search_results.html', context)
