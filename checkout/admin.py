from django.contrib import admin
from .models import Payment
# Register your models here.


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "payment_referance_number",
        "amount",
        "transaction_ref",
        "created_at",
        "payed_at",
        "status",
    ]
