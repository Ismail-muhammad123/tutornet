from django.shortcuts import render
from django.shortcuts import get_object_or_404
from courses.models import Course, Category
from django.contrib.auth import get_user_model

User = get_user_model()


def courses_list(request):

    category_slug = request.GET.get("category", "")
    search_text = request.GET.get("search", "")

    categories = Category.objects.all()
    tutors = User.objects.filter(tutor=True)

    courses = Course.objects.all()[:6]

    if category_slug != "":
        cat = Category.objects.get(slug=category_slug)
        if cat is not None:
            courses = [c for c in courses if c.category == cat]

    if search_text != "":
        courses = [c for c in courses if search_text.lower()
                   in c.title.lower()]

    context = {
        "courses": courses,
        "categories": categories,
        "tutors": tutors,
        "category_slug": category_slug,
        "search_text": search_text
    }

    return render(request, "courses/courses_list.html", context=context)


def course_details(request, slug):
    course = get_object_or_404(Course, slug=slug)
    return render(request, "courses/course_details.html", context={"course": course})


def categories(request):
    categories = Category.objects.all()
    return render(request, "courses/categories.html", context={"categories": categories})


def category_courses(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    courses = Course.objects.filter(category=category)
    context = {
        "courses": courses,
        "category": category
    }
    return render(request, "courses/courses_list.html", context=context)


def tutors(request):
    return render(request, "courses/courses_list.html")
