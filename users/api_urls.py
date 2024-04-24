from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_user, name='api_login_page'),
    path('register', views.register, name='api_register_page'),

    path('update-profile', views.edit_profile, name='api_update_profile'),
    path('my-profile', views.profile, name='api_profile_page'),
    path('logout', views.logout_user, name='api_logout_user'),
]
