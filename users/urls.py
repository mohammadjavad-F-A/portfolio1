from django.urls import path
from .views import *
urlpatterns = [
    path('login/', login_user, name='login_user'),
    path('signup/', sign_up, name='sign_up'),
path('profile/', profile, name='profile'),
    path('logout/', logout_user, name='logout'),
    path('prof_user', prof_user, name='prof_user'),
    path('forgot_pass/', forgot_pass, name='forgot_pass'),
    path('change_password/', change_password, name='change_password'),
]