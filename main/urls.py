from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='index'),
    path('create_project/', create_project, name='create_project'),
    path('confirm_project/<int:pk>', confirms_project, name='confirm_project'),
    path('admins/', admins, name='admins'),
    path('details_project/<int:pk>', details_project, name='details_project'),
    path('about/', about, name='about'),
    path('all_projects/', all_projects, name='all_projects'),
    path('contact/', contact, name='contact'),
    path('deleted_message/<int:pk>/<int:id>', deleted_message, name='deleted_message'),
    path('contact_site/', contact_site, name='contact_site'),
]
