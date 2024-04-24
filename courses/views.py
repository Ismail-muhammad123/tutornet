from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from courses.models import Course, Category, Enrolement
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Coupon, Review
from django.contrib import messages

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


def course_details(request, slug, id): 
    course = get_object_or_404(Course, slug=slug, id=id)
    enrolelements = course.enrolements.filter(student=request.user.id, status=1)
    print(enrolelements)
    return render(request, "courses/course_details.html", context={"course": course, "enroled": len(enrolelements) != 0})


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
    tutors = User.objects.filter(tutor=True)
    context = {
        "tutors": tutors
    }
    return render(request, "courses/tutors.html", context=context)


@login_required
def module_details(request, course_slug, module_slug):
    course = Course.objects.get(slug=course_slug)
    module = course.modules.get(slug=module_slug)
    all_modules = course.modules.all()
    this_index = [n for n in all_modules].index(module)

    context = {
        "course": course,
        "module": module,
    }

    if this_index+1 != len(all_modules):
        context['next_module'] = all_modules[this_index + 1]

    if this_index != 0:
        context['p_module'] = all_modules[this_index-1]

    return render(request, 'courses/module_details.html', context=context)


@login_required
def initialize_enrolement(request, course_slug, course_id):
    try:
        course = Course.objects.get(id=course_id, slug=course_slug)
        enrolement = course.enrolements.filter(student=request.user, status=1)
        if len(enrolement) != 0:
            return redirect(reverse("learn_course_page", kwargs={"course_id": course_id}))
    except:
        pass
    referal_code = request.GET.get("referal_code", "")
    course = get_object_or_404(Course, slug=course_slug, id=course_id)
    if referal_code != "":
        try:
            coupon = Coupon.objects.get(code=referal_code)
            if coupon.is_available():
                total_amount = course.price - (course.price * coupon.discount)
                coupon_is_valid = True

            if total_amount <= course.price and total_amount >= 0:
                print("valid")
                return render(
                    request,
                    "courses/enrole.html",
                    context={
                        "coupon_code": referal_code,
                        "coupon_id": coupon.id,
                        "coupon_valid": coupon_is_valid,
                        "course": course,
                        "discount": coupon.discount * 100,
                        "total_amount": total_amount
                    }
                )
        except Coupon.DoesNotExist:
            pass
    return render(
        request,
        "courses/enrole.html",
        context={
            "coupon_code": referal_code,
            "coupon_valid": False,
            "course": course
        }
    )


@login_required
def confirm_enrole_course(request, course_slug, course_id):

    coupon_code = request.GET.get("coupon_code", "")
    coupon_id = request.GET.get("coupon_id", 0)

    # get course
    course = Course.objects.get(slug=course_slug, id=course_id)
    # get enrolement from payment
    enrolement, created = Enrolement.objects.get_or_create(
        course=course, student=request.user)

    if coupon_code != "" and coupon_id != 0:
        try:
            coupon = Coupon.objects.get(code=coupon_code, id=coupon_id)

            if enrolement.status == 1:
                return redirect(reverse("course_details", kwargs={"slug": course.slug, "id": course.id}))
            else:
                if coupon != None and coupon.is_available():
                    enrolement.coupon = coupon
                    enrolement.total_amount = course.price - \
                        (course.price * coupon.discount)
        except:
            return redirect(reverse("course_details", kwargs={
                "slug": course.slug, "id": course.id}))
    enrolement.total_amount = course.price
    enrolement.save()
    if enrolement.total_amount == 0:
        # if the course is free
        enrolement.status = 1
        enrolement.save()
        return redirect("course_details", kwargs={"slug": enrolement.course.slug, "id": enrolement.course.id})
    else:
        return redirect(reverse("make_payment", kwargs={"enrolement_id": enrolement.id}))


@login_required
def learn(request, course_id, module_id=None):
    course = get_object_or_404(Course, id=course_id)

    enrolements = course.enrolements.filter(student=request.user, status=1)

    enrolement = enrolements[0] if len(enrolements) > 0 else None

    if enrolement == None or enrolement.status != 1:
        messages.add_message(
            request, messages.ERROR, "You are not allowed to access this course, make sure that you have enroled in the course first.")
        return render(request, 'courses/course_details.html', context={"course": course})
    if not course.started():
        messages.add_message(
            request, messages.INFO, "Lessons from this course have not started yet.")
        return render(request, 'courses/course_details.html', context={"course": course, "enroled": enrolement is not None})

    modules = course.modules.all()

    try:
        current_module = course.modules.get(id=module_id)
    except:
        current_module = None

    # if current_module is None:
    #     messages.add_message(
    #         request, messages.ERROR, "The Module you are trying to access is not found.")
    #     return render(request, 'courses/course_details.html', context={"course": course})
    # else:
    context = {
        "course": course,
        "modules": modules,
        "current_module": current_module
    }

    return render(request, "courses/learning_page.html", context=context)



@login_required
def new_review(request):
    if request.method == "POST":
        course_id = request.POST.get('course_id', None)

        if course_id is not None:
            course = get_object_or_404(Course, id=course_id)

            if len(course.reviews.filter(user=request.user.id, course=course.id)) > 0:
                messages.add_message(request, messages.ERROR, "We appriciate your review, but you have already sent a review on this course.")
                return render(request, "courses/new_review.html", context={"course": course})
            
            profession = request.POST["profession"]
            content = request.POST["content"]

            review = Review.objects.create(profession=profession, course =course, user=request.user, content=content)
            review.save()
            messages.add_message(request, messages.SUCCESS, "Your Review hase been added")
            return render(request, "courses/new_review.html", context={"course": course})
        else:
            return redirect("/")
  
    course_id = request.GET.get('course_id', None)
    if course_id is not None:
        course = get_object_or_404(Course, id=course_id)
        return render(request, "courses/new_review.html", context={"course": course})
    return redirect("/")
  