from django.urls import path

from . import views

app_name = '' ## Default App
urlpatterns = [
    path('', views.index, name='index'),
    path('pb/<int:pbID>/section/<int:sectionID>/create', views.addPage, name="addPage"),
    path('pb/<int:pbID>/section/<int:sectionID>/addExisting', views.addExistingPage, name="addExistingPage"),
    path('pb/<int:pbID>', views.playbook, name="playbook"),
    path('pb/<int:pbID>/delete', views.deletePlaybook, name="deletePlaybook"),
    path('pb/<int:pbID>/addSection', views.addSection, name="addSection"),
    path('pb/section/<int:sectionID>/updatePagePosition', views.updatePagePosition, name="updatePagePosition"),
    path('pb/section/<int:sectionID>/delete', views.deleteSection, name="deleteSection"),
    path('pb/section/<int:sectionID>/page/<int:pageID>/delete', views.deletePage, name="deletePage"),
    path('pb/page/<int:pageID>', views.pageContent, name="pageContent"),
    path('pb/page/<int:sectionID>/new', views.newPage, name="newPage"),
    path('pb/page/<int:pageID>/edit/<int:sectionID>', views.editPage, name="editPage"),
    path('pb/page/<int:pageID>/update/<int:sectionID>', views.updatePage, name="updatePage"),
    path('api/pb/prefetch', views.apiPrefetchSource, name="apiPrefetchSource"),
    path('api/pb/serverFiles', views.apiServerFileOptions, name="apiServerFileOptions"),
    path('api/pb/updateStatus/<int:pageID>', views.apiPageUpateStatus, name="apiPageUpateStatus"),
    path('api/pb/updatePage/<int:pageID>', views.apiUpdatePage, name="apiUpdatePage"),
    path('api/pb/prefetchUpdatePage/<int:pageID>', views.apiPrefetchUpdatePage, name="apiPrefetchUpdatePage"),
    path('api/pb/pageTitle/<int:pageID>', views.apiGetPageTitle, name="apiGetPageTitle"),
    path('api/search/', views.apiSearchPlaybooks, name="apiSearchPlaybooks"),
]
