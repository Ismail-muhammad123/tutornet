from django.shortcuts import render
from django.shortcuts import get_object_or_404
from courses.models import Course

# Create your views here.


def courses_list(request):

    courses = Course.objects.all()[:6]

    context = {
        "courses": courses
    }

    return render(request, "courses/courses_list.html", context=context)


def course_details(request, slug):
    course = get_object_or_404(Course, slug=slug)
    return render(request, "courses/course_details.html", context={"course": course})


def categories(request):
    pass


def category_courses(request, slug):
    pass
