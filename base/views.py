from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from courses.models import Category, Course
from .models import NewsLetterList, ContactMessage
from django.urls import reverse
from django.contrib import messages
# Create your views here.

User = get_user_model()


def index(request):
    top_categories = Category.objects.all()

    if len(top_categories) > 5:
        top_categories = top_categories[:5]

    top_tutors =  User.objects.filter(tutor=True) 

    if len(top_tutors) > 5:
        top_tutors = top_tutors[:5]

    top_courses = Course.objects.all()

    if len(top_courses) > 5:
        top_courses = top_courses[:5]

    context = {
        "top_categories": top_categories,
        "top_tutors": top_tutors,
        "top_courses": top_courses,
    }

    return render(request, 'base/index.html', context=context)


def about(request):
    tutors = User.objects.filter(tutor=True)

    # tutors = [tutor for tutor in tutors if tutor.courses.count() > 10]

    context = {
        "tutors": tutors
    }
    return render(request, 'base/about.html', context=context)


def contact(request):
    if request.method == "POST":
        email = request.POST.get("email", "")
        name = request.POST.get("name", "")
        subject = request.POST.get("subject", "")
        message = request.POST.get("message", "")

        if email != "" and name != "" and subject != "" and message != "":
            try:
                contact_message = ContactMessage(
                    name=name,
                    email=email,
                    subject=subject,
                    message=message
                )
                contact_message.save()
                messages.add_message(
                    request, messages.SUCCESS, "Thank You for sending us a message. We will get back you you soon.")

            except:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Sorry, we are unable to recieve your message, please check and try again."
                )
        else:
            messages.add_message(
                request, messages.ERROR, "All fields must be provided.")
    return render(request, 'base/contact.html')


def send_subscrib_success_email(email):
    pass


def send_unsubscribe_success_email(email):
    pass


def subscribe_to_newsletter(request):
    email = request.GET['email']

    if email != None and email != '':
        n = NewsLetterList.objects.create(email=email)
        n.save()
        send_subscrib_success_email(email)
        messages.add_message(request, messages.SUCCESS,
                             "You have successfully sibscribe to our newsletter.")
    else:
        messages.add_message(request, messages.ERROR,
                             "unable to subscribe you to our newsletter")
    return render(request, "base/index.html")


def unsubscribe_to_newsletter(request):
    email = request.GET['email']

    if email != None and email != '':
        n = NewsLetterList.objects.create(email=email)
        n.save()
        send_unsubscribe_success_email(email)
        messages.add_message(request, messages.SUCCESS,
                             "You have successfully been unsibscribe to our newsletter.")
    else:
        messages.add_message(request, messages.ERROR,
                             "unable to unsubscribe you from our newsletter")
    return render(request, "base/index.html")
