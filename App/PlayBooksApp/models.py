from django.db import models
from django.contrib.auth.models import User


from PlayBooksWeb.models import IncludedFolder

class Playbook(models.Model):
    name = models.CharField(max_length=500)
    cover_img = models.TextField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    @classmethod
    def user_all(self, user):
        return self.objects.filter(creator=user)
    
    def user_sections(self, user):
        return self.sections.filter(creator=user)

    ## Only creator can delete Playbook
    def can_delete(self, user):
        return (user == self.creator)

    def __str__(self):
        return "name='%s', created='%s', last_modified='%s'" %(self.name, self.created_at, self.last_modified)


class Playpage(models.Model):
    SOURCE_HTTP = "HTTP"
    SOURCE_UPLOAD = "UPLOAD"
    SOURCE_DISK = "DISK" 
    SOURCE_TEXT = "TEXT"

    title = models.CharField(max_length=500)
    source = models.TextField(null=True, blank=True)
    source_type = models.CharField(max_length=500, default=SOURCE_HTTP)
    offline_store = models.TextField(null=True, blank=True)
    included_folder = models.ForeignKey(IncludedFolder, on_delete=models.SET_NULL, null=True, blank=True)
    check_updates = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    ## Access = Read + Write
    def can_access(self, user):
        return ( user == self.creator )
    
    ## Change Position
    def can_change_position(self, user):
        return self.can_access(user)

    ## Only creator can delete Pages
    def can_delete(self, user):
        return (user == self.creator)
    
    def can_be_updated(self):
        return self.source_type in [self.SOURCE_DISK, self.SOURCE_HTTP]

    def playbooks(self):
        return Playbook.objects.filter(section__pages__id=self.id)

    @classmethod
    def accessible_pages(self, user):
        return [ page for page in self.objects.all() if page.can_access(user) ]

    def save_model(self, request, obj, form, change):
        if( request.user and not obj.pk ):
            # Only set added_by during the first save.
            obj.creator = request.user
        super().save_model(request, obj, form, change)


    def set_position(self, position, sectionID):
        try:
            section_content = self.section_contents.get(section=sectionID)
            section_content.page_position = position
            section_content.save()
        except Exception as e:
            return e
        else:
            return True

    def __str__(self):
        return "title='%s', created='%s', last_modified='%s'" %(self.title, self.created_at, self.last_modified)


class PlaybookSection(models.Model):
    class Meta:
        ordering = ['section_position']
    
    name = models.CharField(max_length=100)
    section_position = models.PositiveIntegerField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    playbook = models.ForeignKey(
        Playbook, 
        on_delete=models.CASCADE, 
        related_name='sections',
        related_query_name="section",)
    pages = models.ManyToManyField(
        Playpage,
        through='SectionContent', through_fields=('section', 'playpage'), 
        related_name='sections',
        related_query_name="section")

    ## Only creator can delete Section
    def can_delete(self, user):
        return (user == self.creator)
    
    def pages_sorted(self):
        return self.pages.all().order_by('section_contents__page_position')

    def last_page_position(self):
        position = 0
        try:
            position = self.section_contents.order_by('page_position').last().page_position
        except:
            ## if error, pass and go with 0
            pass
        return position
        #return self.section_contents.order_by('page_position').last().page_position
    
    def append_page(self, page):
        position = self.last_page_position() or 0
        return self.pages.add( page, through_defaults={ 'page_position': position })

    def __str__(self):
        return "name='%s' position='%s'" %(self.name, self.section_position)


class SectionContent(models.Model):
    class Meta:
        ordering = ['page_position']

    section = models.ForeignKey(
        PlaybookSection, 
        on_delete=models.CASCADE, 
        related_name='section_contents',
        related_query_name="section_contents"
    )
    playpage = models.ForeignKey(
        Playpage, 
        on_delete=models.CASCADE,
        related_name='section_contents',
        related_query_name="section_contents"
    )
    page_position =  models.PositiveIntegerField(default=0)

