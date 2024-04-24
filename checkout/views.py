from datetime import datetime
from django.conf import settings
from django.utils.timezone import make_aware
from json import JSONDecoder
from pprint import pprint
from django.shortcuts import render, redirect
from django.conf import settings
import uuid
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required, user_passes_test

from courses.models import Enrolement

from .models import Payment
import requests
from django.contrib import messages
from django.urls import reverse
from django.http import Http404, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required


@login_required
def checkout(request, enrolement_id):
    unique_id = str(uuid.uuid4())
    verification_url = settings.REDIRECT_URL
    # device = request.COOKIES['device']
    enrolement = get_object_or_404(Enrolement, id=enrolement_id)
    if enrolement.student == request.user:
        email = request.user.email
        full_name = request.user.get_full_name()
        phone_number = request.user.mobile_number

        payment = Payment.objects.create(
            payment_referance_number=unique_id,
            amount=enrolement.total_amount
        )

        # if not created:
        #     if payment.status == 2:
        #         messages.add_message(
        #             request, messages.INFO, "You have already completed the payment for this course.")
        #         return redirect(reverse("course_details", kwargs={"slug": enrolement.course.slug, "id": enrolement.course.id}))

        payment.user = request.user

        payment.save()

        url = settings.PAYMENT_GATEAWAY_URL
        secret_key = settings.PAYMENT_GATEAWAY_SECRET_KEY

        headers = {"Authorization": f"Bearer {secret_key}"}

        print(f"Amount: {enrolement.total_amount}")

        data = {
            "reference": unique_id,
            'email': email,
            "amount": enrolement.total_amount * 100,
            "currency": "NGN",
            "callback_url": verification_url,
            "metadata": {
                "enrolement_id": enrolement.id,
                "customer": {
                    "email": email,
                    "phone_number": phone_number,
                    "name": full_name
                },
            },
        }
        res = requests.post(url, headers=headers, json=data)
        response = res.json()
        print(response)
        enrolement.payment = payment
        enrolement.save()
        if response['status'] == True:
            return redirect(response['data']['authorization_url'])
        else:
            payment.delete()
            messages.add_message(
                request, messages.ERROR, "Course Enrolement Failed!")
            return render(request, "courses/course_details.html", context={"course": enrolement.course})
    else:
        raise Http404()


def verify_payment(request):
    headers = {"Authorization": f"Bearer {settings.PAYMENT_GATEAWAY_SECRET_KEY}"}
    data = request.GET

    tx_ref = data['trxref']
    response = requests.get(
        settings.PAYMENT_VERIFICATION_URL + tx_ref, headers=headers)
    # print(response.status_code)
    if response.status_code == 200:
        res = response.json()
        status = res['data']['log']['success']
        # print(status)
        if status:
            print(res['data']['metadata'])
            enrolement_id = res['data']['metadata']['enrolement_id']
            # get order object
            enrolement = get_object_or_404(Enrolement, id=enrolement_id)
            enrolement.status = 1
            enrolement.save()

            # get payment object and update its attributes
            payment = enrolement.payment
            now = datetime.now()
            aware_datetime = make_aware(now)
            payment.payed_at = aware_datetime
            payment.status = 2
            payment.transaction_ref = tx_ref
            payment.save()

            # redirect to order-tracking page
            return redirect(reverse('profile_page'))
        else:
            print(res['data']['metadata'])
            enrolement = Enrolement.objects.get(id=enrolement_id)
            enrolement.delete()
            # messages.add_message(
            #     request, messages.ERROR, f"Payment for course {enrolement.course.title} failed")
            return redirect(reverse("course_details", kwargs={"slug": enrolement.course.slug, "id": enrolement.course.id}))

    else:

        return redirect(reverse("courses_list"))


def payment_hook():
    pass
