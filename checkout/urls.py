from django.urls import path, include
from .views import checkout, verify_payment

urlpatterns = [
    path("pay/<str:enrolement_id>", checkout, name="make_payment"),
    path("verify/", verify_payment, name="verify_payment")
]
