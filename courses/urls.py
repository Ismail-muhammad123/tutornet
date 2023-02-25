from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.courses_list, name="courses_list"),
    path('course/<str:slug>', views.course_details, name="course_details"),
    path('categories', views.categories, name="categories_list"),
    path('category/<str:category_slug>', views.category_courses,
         name="category_courses_list"),

    path('tutors/', views.tutors, name="tutors_list"),
]
