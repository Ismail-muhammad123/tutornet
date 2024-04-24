from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Payment(models.Model):

    STATUS_CHOICES = [
        (0, "failed"),
        (1, "Pending"),
        (2, "Success"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="payments")
    payment_referance_number = models.CharField(max_length=200)
    amount = models.FloatField()
    transaction_ref = models.CharField(max_length=250, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payed_at = models.DateTimeField(null=True)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=1)

    # device = models.CharField(
    #     max_length=100, null=True, blank=True, default="")
