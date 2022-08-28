from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.courses_list, name="courses_list"),
    path('<str:slug>', views.course_details, name="course_details"),
    path('categories', views.categories, name="categories_list"),
    path('categories/<str:slug>', views.category_courses, name="category_courses_list"),
]
