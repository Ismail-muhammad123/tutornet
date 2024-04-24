from django.urls import path
from . import views

urlpatterns = [
    path('',  views.index, name='home_page'),
    path('about',  views.about, name='about_page'),
    path('contact',  views.contact, name='contact_page'),
    path('newsletter/subscribe',  views.subscribe_to_newsletter,
         name='subscribe_newsletter'),
    path('newsletter/unsubscribe',  views.unsubscribe_to_newsletter,
         name='unsubscribe_newsletter'),
]
