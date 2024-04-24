from tabnanny import verbose
from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "date_added",
        "cover_photo",
    ]

    fields = [
         "name",
         "cover_photo",
    ]

    class Meta:
        verbose_plural_name = "Categories"

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "added_at",
    ]

    fields = [
          "name",
        "category",
    ]



@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    def category(self, obj):
        return obj.sub_category.category.name
    

    list_display = [
        "name",
        "category",
        "sub_category",
        "added_at",
    ]

    fields = [
              "name",
        "sub_category",
    ]

    class Meta:
        verbose_plural_name = "Topics"

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        "slug",
        "title",
        "price",
        "language",
        "description",
        "tutor",
        "category",
        "sub_category",
        "topic",
        "cover_photo",
        "intoduction_video",
        "added_at",
        "start_date",
    ]

    fields = [
        "title",
        "price",
        "language",
        "description",
        "tutor",
        "category",
        "sub_category",
        "topic",
        "cover_photo",
        "intoduction_video",
        "start_date",
    ]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "course",
        "added_at",
        "description",
    ]


@admin.register(Enrolement)
class EnrolementAdmin(admin.ModelAdmin):
    list_display = [
        "course",
        "student",
        "status",
        "enroled_at",
        "coupon",
        "payment",
        "total_amount",
    ]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display =[
        "user",
        "course",
        "created_at",
        "content",
    ]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    def percent_discount(self, obj):
        return f"{obj.discount * 100}%"

    def total_enrolements(self, obj):
        return obj.enrolements.count()

    list_display = [
        "course",
        "percent_discount",
        "max_usage",
        "total_enrolements",
        "code",
        "created_at",
    ]


@admin.register(SupportDocument)
class SupportDocumentAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        "type",
        "file",
        "module",
        "added_at",
    ]
