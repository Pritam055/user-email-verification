from django.urls import path
from django.urls.resolvers import URLPattern 

from .views import home , register, verify_token, login_user, error_page, logout_user, forgetPassword, changePassword

urlpatterns = [ 
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('verify/<str:token>/', verify_token, name='verify-token'),
    path('login/', login_user, name='login'),
    path('error/', error_page, name='error'),
    path('logout/', logout_user, name='logout'),
    path('forget-password/', forgetPassword, name='forget-password' ),
    path('change-password/<str:token>/', changePassword, name='change-password'),
]