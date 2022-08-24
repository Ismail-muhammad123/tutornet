from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_user, name='login_page'),
    path('register', views.register, name='register_page'),

    path('not_verified', views.not_verified, name='not_verified_page'),
    path('verify-account/<str:id>/<str:token>',
         views.verify_account, name='verify_account_page'),

    path('my-profile', views.profile, name='profile_page'),
    path('logout', views.logout_user, name='logout_user'),

    path('forget-password', views.forget_password, name='reset_password'),
    path('set_new-password', views.new_password, name='new_password'),
]
