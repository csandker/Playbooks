from django import forms
from django.forms import ModelForm, ChoiceField
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from .models import Playpage, PlaybookSection, Playbook
from .request import URLRequester
from .markdown import MarkdownParser
from .source_resolver import SourceResolver

from PlayBooksWeb.models import IncludedFolder


class ChoiceFieldNoValidation(ChoiceField):
    DEFAULT_CHOICE = ( ('-', (('', '-- Choose Folder --'),)),)

    def validate(self, value):
        pass

class PlaypageForm(ModelForm):
    INIT_SOURCE_TYPE = None

    class Meta:
        model = Playpage
        fields = ['title','source_type', 'check_updates']
        help_texts = {
            'title': _("Title of your Page. Keep this short but significant"),
        }
        widgets = {
            'title': forms.TextInput(attrs={'required': '', 'class': 'form-control'}),
            'check_updates': forms.CheckboxInput( attrs={'data-toggle': 'toggle', 'class': 'update-toggle'} )
        }

    def __init__(self, user, *args, **kwargs):
        super(PlaypageForm, self).__init__(*args, **kwargs)
        if( not self.instance.pk ):
            self.instance.creator = user
        
        if( self.INIT_SOURCE_TYPE ):
            self.instance.source_type = self.INIT_SOURCE_TYPE
            self['source_type'].initial = self.INIT_SOURCE_TYPE

        ## HTTP UPLOAD FIELD
        http_initial = self.instance.source if ( self.instance and self.instance.source_type == Playpage.SOURCE_HTTP ) else '' 
        http_source = forms.CharField(required=False, label="HTTP Resource", initial=http_initial )
        http_source.help_text = _("Enter a HTTP URL to fetch Markdown Text from, e.g. Raw Github Pages.")
        http_source.widget = forms.TextInput(attrs={
            "data-event": 'urlPrefetch', 
            "data-url-prefetch": reverse('apiPrefetchSource'),
            'class': 'full-width',
            "placeholder": "https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1170/T1170.md"
        })
        self.fields['http_source'] = http_source
        ## FILE UPLOAD FIELD
        file_initial = self.instance.source if ( self.instance and self.instance.source_type == Playpage.SOURCE_UPLOAD ) else ''
        file_source = forms.FileField(required=False, label="File Upload", initial=file_initial)
        file_source.help_text = _("Upload a Markdown file")
        file_source.widget = forms.FileInput(attrs={
            "data-event": 'urlPrefetch', 
            "data-url-prefetch": reverse('apiPrefetchSource'),
            'class': 'form-control'
        })
        self.fields['file_source'] = file_source
        ## DISK UPLOAD FIELD
        ### DISK FILES
        if( 
            self.instance.source_type == Playpage.SOURCE_DISK and
            self.instance and 
            self.instance.included_folder and
            self.instance.included_folder.id and
            self.instance.source
        ):
            allowedExtensions = MarkdownParser.ALLOWED_FILE_EXTENSIONS
            included_folder_ID = self.instance.included_folder.id
            included_folder_path_choices = IncludedFolder.list_allowed_files(included_folder_ID, allowedExtensions)
            included_folder_path_initial = self.instance.source
        else:
            included_folder_path_choices = ChoiceFieldNoValidation.DEFAULT_CHOICE
            included_folder_path_initial = ''
        included_folder_path = ChoiceFieldNoValidation(required=False, label='File', initial=included_folder_path_initial)
        included_folder_path.help_text = _("Chose a File From Disk As Source")
        included_folder_path.widget = forms.Select(choices=included_folder_path_choices, attrs={
            'class': 'form-control',
            'data-event': 'urlPrefetch', 
            'data-url-prefetch': reverse('apiPrefetchSource'),
            'data-live-search': 'true'
        })
        self.fields['included_folder_path'] = included_folder_path
        ### DISK Folders
        disk_folder_choices = [('', '-- Choose --')] + [ (folder.id, folder.name) for folder in IncludedFolder.objects.all() ] # 
        included_folder_initial = self.instance.included_folder.id if ( self.instance.source_type == Playpage.SOURCE_DISK and self.instance and self.instance.included_folder ) else ''
        included_folder = forms.ChoiceField(required=False, label='Folder', initial=included_folder_initial)
        included_folder.choices = disk_folder_choices
        included_folder.help_text = _("Choose a Folder From Disk To Select a Markdown File")
        included_folder.widget = forms.Select(choices=disk_folder_choices, attrs={
            'data-event': 'diskFolder', 
            'data-update-target': self['included_folder_path'].auto_id,
            'data-url-fileoptions': reverse('apiServerFileOptions'),
            'class': 'form-control'
        })
        self.fields['included_folder'] = included_folder
        ## PASTE UPLOAD
        text_source_initial = self.instance.offline_store if ( self.instance ) else ''
        text_source = forms.CharField(required=False, label=False, initial=text_source_initial )
        text_source.help_text = _("Write Markdown Yourself")
        text_source.widget = forms.Textarea(attrs={
            "data-event": 'urlPrefetch', 
            "data-url-prefetch": reverse('apiPrefetchSource'), 
            "placeholder": "Start Typing...",
            "class": "hidden"
        })
        self.fields['text_source'] = text_source

        ## FIELD Order
        self.field_order = ['title', 'source_type', 'http_source', 'file_source', 'included_folder', 'included_folder_path', 'text_source', 'check_updates']
        self.order_fields(self.field_order)

        self.source_options =  [
            {'name': 'HTTP', 'source_type': self.instance.SOURCE_HTTP, 'source_field': self['source_type'].auto_id,
                'allowed_fields': [
                    self['title'].auto_id, self['check_updates'].auto_id, self['http_source'].auto_id
                ]
            },
            {'name': 'FILE UPLOAD', 'source_type': self.instance.SOURCE_UPLOAD, 'source_field': self['source_type'].auto_id,
                'allowed_fields': [
                    self['title'].auto_id, self['file_source'].auto_id
                ]
            }
            ,
            {'name': 'FROM SERVER', 'source_type': self.instance.SOURCE_DISK , 'source_field': self['source_type'].auto_id,
                'allowed_fields': [
                    self['title'].auto_id, self['check_updates'].auto_id, self['included_folder'].auto_id, self['included_folder_path'].auto_id
                ]
            },
            {'name': 'TEXT INPUT', 'source_type': self.instance.SOURCE_TEXT , 'source_field': self['source_type'].auto_id,
                'allowed_fields': [
                    self['title'].auto_id, self['text_source'].auto_id, "page_update_modal_editablediv"
                ]
            }

        ]



    def validate_file_source(self):
        file_source = self['file_source'].data
        ## check existing
        if( not file_source  ):
            if( hasattr(self._errors, 'get') and not self._errors.get('file_source') ):
                emsg = "File Source is required"
                self.add_error('file_source', emsg)
            return False
        ## check file upload content type 
        if( hasattr(file_source, 'content_type') and not (file_source.content_type in MarkdownParser.ALLOWED_MIME_TYPES) ):
            if( hasattr(self._errors, 'get') and not self._errors.get('file_source') ):
                emsg = "File Source MimeType is not allowed. Content Type is %s" %file_source.content_type
                self.add_error('file_source', emsg)
            return False 
        ## check mime type based on content
        try:
            import magic
            import copy
            ## make a deep copy
            buffer_copy = copy.deepcopy(file_source)
            ## reset the read cursor
            buffer_copy.seek(0)
            prober = magic.Magic(mime=True)
            buffer = buffer_copy.read().decode('utf-8', errors='ignore')
            probed_content_type = prober.from_buffer(buffer)
            if( not (probed_content_type in MarkdownParser.ALLOWED_MIME_TYPES) ):
                if( hasattr(self._errors, 'get') and not self._errors.get('file_source') ):
                    emsg = "File Source MimeType is not allowed. Mime Type is %s" %probed_content_type
                    self.add_error('file_source', emsg)
                return False 
        except:
            ## pass along
            pass
        
        return True

    def validate_http_source(self):
        url = self['http_source'].data
        ## Check if existing
        if( not url ):
            if( hasattr(self._errors, 'get') and not self._errors.get('http_source') ):
                emsg = "HTTP Resource is required"
                self.add_error('http_source', emsg)
            return False 
        else:
            ## Check if valid URL
            urlvalidator = URLValidator(schemes=['http', 'https'])
            try:
                urlvalidator(url)
            except ValidationError as e:
                if( hasattr(self._errors, 'get') and not self._errors.get('http_source') ):
                    emsg = "Invalid URL scheme. Only http:// https:// is allowed"
                    self.add_error('http_source', emsg)
                return False
            else:
                requester = URLRequester(url)
                requester.request()
                valid_response = requester.is_valid_response()
                if( not valid_response ):
                    ## Add error if not already added
                    if( hasattr(self._errors, 'get') and not self._errors.get('http_source') ):
                        status_code = requester.get_status_code()
                        emsg = "Received Invalid Server Response. Status Code was: '%s'" %(status_code)
                        self.add_error('http_source', emsg)
                    return False
        return True

    def validate_included_folder(self):
        ## Validate folder
        include_fodlerID = self['included_folder'].data
        if( not include_fodlerID ):
            if( hasattr(self._errors, 'get') and not self._errors.get('included_folder') ):
                emsg = "Not a valid choice."
                self.add_error('included_folder', emsg)
            return False
        objs = IncludedFolder.objects.filter(pk=include_fodlerID)
        if objs.count() != 1:
            if( hasattr(self._errors, 'get') and not self._errors.get('included_folder') ):
                emsg = "Not a valid choice."
                self.add_error('included_folder', emsg)
            return False
        return True

    def validate_included_folder_path(self):
        ## Validate path
        include_folder_path = self['included_folder_path'].data
        if( not include_folder_path ):
            if( hasattr(self._errors, 'get') and not self._errors.get('included_folder_path') ):
                emsg = "Not a valid choice."
                self.add_error('included_folder_path', emsg)
            return False
        if( ("../" in include_folder_path) or ("..\\" in include_folder_path) ):
            if( hasattr(self._errors, 'get') and not self._errors.get('included_folder_path') ):
                emsg = "Illegal characters contained in choice."
                self.add_error('included_folder_path', emsg)
            return False
        
        ## Check included Folder existing
        included_folder = self['included_folder'].data
        if( not included_folder ):
            if( hasattr(self._errors, 'get') and not self._errors.get('included_folder_path') ):
                emsg = "No Folder has been selected"
                self.add_error('included_folder_path', emsg)
            return False
        
        ## Check file path
        included_folder_obj = IncludedFolder.objects.get( pk=included_folder )
        folder_path = included_folder_obj.path
        folder_path += '' if folder_path.endswith('/') else '/'
        file_path = "%s%s" %(folder_path, include_folder_path)
        if( not IncludedFolder.valid_file_path(file_path) ):
            if( hasattr(self._errors, 'get') and not self._errors.get('included_folder_path') ):
                emsg = "File not found on Server"
                self.add_error('included_folder_path', emsg)
            return False
        return True

    def validate_text_source(self):
        text_source = self['text_source'].data
        if( not text_source ):
            if( hasattr(self._errors, 'get') and not self._errors.get('text_source') ):
                emsg = "Required Field"
                self.add_error('text_source', emsg)
            return False
        return True

    def is_valid(self):
        ### Custom Validations
        valid_super = super(ModelForm, self).is_valid()
        source_type = self['source_type'].data
        valid_source = self.validate_source_type(source_type)

        return (valid_super and valid_source)

    def validate_source_type(self, source_type):
        if( source_type == Playpage.SOURCE_UPLOAD):
            return self.validate_file_source()
        elif( source_type == Playpage.SOURCE_HTTP ):
            return self.validate_http_source()
        elif( source_type == Playpage.SOURCE_DISK ):
            return ( self.validate_included_folder() and self.validate_included_folder_path() )
        elif( source_type == Playpage.SOURCE_TEXT ):
            return self.validate_text_source()

    def get_included_folder_path_options(self):
        return self.fields['included_folder_path'].widget.choices

    def clean(self):
        ## Parent Clean
        super().clean()
        ## Custom Cleaning
        source_type = self.cleaned_data['source_type']
        ## Setting Data
        if( source_type == Playpage.SOURCE_UPLOAD):
            valid = self.validate_file_source()
            if( valid ):
                ## can't be updated
                self.instance.check_updates = False
                self.cleaned_data['check_updates'] = False
                 ## can't have include folder
                self.instance.included_folder = None
                self.cleaned_data['included_folder'] = None
                ## content
                self.instance.source = self.cleaned_data['file_source']
                self.instance.offline_store = self.cleaned_data['file_source'].read().decode('utf-8', errors='ignore')
        
        elif( source_type == Playpage.SOURCE_HTTP ):
            valid = self.validate_http_source()
            if( valid ):
                ## can't have include folder
                self.instance.included_folder = None
                self.cleaned_data['included_folder'] = None
                ## content
                url = self.cleaned_data.get('http_source', '')
                resolver = SourceResolver(self.instance)
                response = resolver.resolve_from_http(url)
                self.instance.source = self.cleaned_data['http_source']
                if( response ):
                    self.instance.offline_store = response

        elif( source_type == Playpage.SOURCE_DISK ):
            valid_included_folder = self.validate_included_folder()
            if( valid_included_folder ):
                selected_included_folder = self.cleaned_data['included_folder']
                if( selected_included_folder ):
                    allowedExtensions = MarkdownParser.ALLOWED_FILE_EXTENSIONS
                    newChoices = IncludedFolder.list_allowed_files(selected_included_folder, allowedExtensions)
                    self.fields['included_folder_path'].widget.choices = newChoices
                    self.fields['included_folder_path'].choices = newChoices
                    self.instance.included_folder = IncludedFolder.objects.get( pk=selected_included_folder )
            else:
                ## Reset to default choice
                newChoices = ChoiceFieldNoValidation.DEFAULT_CHOICE
                self.fields['included_folder_path'].widget.choices = newChoices
                self.fields['included_folder_path'].choices = newChoices
            valid_included_folder_path = self.validate_included_folder_path()
            if( valid_included_folder and valid_included_folder_path ):
                selected_included_folder = self.cleaned_data['included_folder']
                selected_included_folder_path = self.cleaned_data['included_folder_path'] 
                if( selected_included_folder_path ):
                    self.instance.source = selected_included_folder_path
                    resolver = SourceResolver(self.instance)
                    content = resolver.resolve_from_disk(selected_included_folder, selected_included_folder_path)
                    if( content ):
                        self.instance.offline_store = content

        elif( source_type == Playpage.SOURCE_TEXT ):
            valid_text_source = self.validate_text_source()
            if( valid_text_source ):
                ## Keep original source type if exiting
                if( self.instance.pk ):
                    self.cleaned_data['source_type'] = self.instance.source_type
                ## offline store
                self.instance.offline_store = self.cleaned_data['text_source']

        return self.cleaned_data


class TEXTPLaypageForm(PlaypageForm):
    INIT_SOURCE_TYPE = Playpage.SOURCE_TEXT


class PlaybookSectionForm(ModelForm):

    class Meta:
        model = PlaybookSection
        fields = ['name']
        help_texts = {
            'name': _("Enter a name for a new Section"),
        }
        widgets = {'name': forms.TextInput(
            attrs = {
                'autocomplete': 'off',
                'placeholder': 'New Section Name', 
                'class': 'form-control'
            }
        )}

    def __init__(self, user, *args, **kwargs):
        super(PlaybookSectionForm, self).__init__(*args, **kwargs)
        if( not self.instance.pk ):
            self.instance.creator = user

class PlaybookAddPageForm(forms.Form):
    page = forms.ChoiceField(
        label = "Add Existing Page",
        help_text = "Add existing Page",
        widget = forms.Select(
            attrs = {
                'class': 'form-control selectpicker',
                'data-live-search': 'true'
            }
        )
    )

    def __init__(self, user, *args, **kwargs):
        super(PlaybookAddPageForm, self).__init__(*args, **kwargs)
        accessible_pages = Playpage.accessible_pages(user)
        choices = [ (page.id, page.title) for page in accessible_pages ]
        self.fields['page'].choices = choices
        self.fields['page'].widget.choices = choices

class PlaybookForm(ModelForm):
    class Meta:
        model = Playbook
        fields = ['name']
        help_texts = {
            'name': _("Enter a name for a new PlayBook"),
        }
        widgets = {'name': forms.TextInput(
            attrs = {
                'autocomplete': 'off',
                'placeholder': 'New Playbook Name', 
                'class': 'form-control'
            }
        )}


    def __init__(self, user, *args, **kwargs):
        super(PlaybookForm, self).__init__(*args, **kwargs)
        if( not self.instance.pk ):
            self.instance.creator = user