from django.urls import path
from . import views

urlpatterns = [
    path('', views.courses_list, name="courses_list"),

    path('course/<str:slug>/<int:id>',
         views.course_details, name="course_details"),

     path('course/review/new',
         views.new_review, name="add_new_review"),

    path('course/enrole/confirm/<int:course_id>/<str:course_slug>',
         views.confirm_enrole_course, name="complete_enrole_course"),

    path('course/enrole/init/<int:course_id>/<str:course_slug>',
         views.initialize_enrolement, name="enrole_course"),

    path('categories', views.categories, name="categories_list"),

    path('category/<str:category_slug>', views.category_courses,
         name="category_courses_list"),

    path('course/<int:course_id>/<str:course_slug>/modules/<str:module_slug>',
         views.module_details, name="module_details_page"),

    path('learn/course/<int:course_id>',
         views.learn, name="learn_course_page"),

    path('learn/course/<int:course_id>/modules/<int:module_id>',
         views.learn, name="learn_course_page"),




    path('tutors/', views.tutors, name="tutors_list"),
]
