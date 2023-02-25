from django.shortcuts import render
from django.contrib.auth import get_user_model

# Create your views here.

User = get_user_model()


def index(request):
    return render(request, 'base/index.html')


def about(request):
    tutors = User.objects.filter(tutor=True)

    # tutors = [tutor for tutor in tutors if tutor.courses.count() > 10]

    context = {
        "tutors": tutors
    }
    return render(request, 'base/about.html', context=context)


def contact(request):
    return render(request, 'base/contact.html')
