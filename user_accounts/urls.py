
from django.urls import path

from user_accounts.views import LoginUserView, ProfileView, RegisterUserView

urlpatterns = [    
     
    path("createuser/", RegisterUserView.as_view()), 
    path("login/", LoginUserView.as_view()), 
    path("profile/", ProfileView.as_view()), 
    
]
