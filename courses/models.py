from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from checkout.models import Payment
import datetime

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    cover_photo = models.ImageField(upload_to="course_categories")
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

class SubCategory(models.Model):
    slug = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, related_name="sub_categories", on_delete=models.SET_NULL, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Sub Categories"


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)

    
    def __str__(self) -> str:
        return self.name + ' - ' + self.category.name
    

class Topic(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, related_name='topics', on_delete=models.SET_NULL, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Topic, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name + ' - ' + self.sub_category.name + ' - ' + self.sub_category.category.name

class Course(models.Model):

    LANGUAGES_CHOICES = (
        ('en', 'English'),
        ('ha', 'Hausa'),
        ('yo', 'Yoruba'),
        ('ig', 'Igbo'),
        ('pcm', 'Pidgin English'),
        ('ar', 'Arabic'),
        ('sw', 'Swahili'),
        ('am', 'Amharic'),
        ('so', 'Somali'),
        ('zu', 'Zulu'),
        ('fr', 'French'),
        ('pt', 'Portuguese'),
        ('af', 'Afrikaans'),
        ('wo', 'Wolof'),
        ('om', 'Oromo'),
        ('ti', 'Tigrinya'),
        ('ber', 'Berber'),
    )

    slug = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    language = models.CharField(max_length=5, choices=LANGUAGES_CHOICES, default='en')
    description = models.TextField(default="")
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses",  limit_choices_to={"tutor": True})
    category = models.ForeignKey( Category, on_delete=models.CASCADE, related_name='courses')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, related_name='courses', null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, related_name='courses', null=True)
    cover_photo = models.ImageField(upload_to="courses")
    intoduction_video = models.URLField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    def get_full_duration(self):
        return 10
    
    def started(self):
       self.start_date.date() > datetime.datetime.now().date()

class Module(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="modules")
    added_at = models.DateTimeField(auto_now_add=True)
    video = models.URLField(null=True, blank=True)
    description = models.TextField()
    slug = models.CharField(max_length=200, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Module, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title + '-' + self.course.title


class SupportDocument(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    file = models.FileField(upload_to="course_support_files")
    added_at = models.DateTimeField(auto_now_add=True)
    module = models.ForeignKey(
        Module, on_delete=models.SET_NULL, null=True,  related_name="resources")

    def __str__(self) -> str:
        return self.name


class Coupon(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    discount = models.FloatField(default=0)
    max_usage = models.PositiveIntegerField(default=0)
    code = models.CharField(max_length=12, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.code

    def is_available(self):
        return self.enrolements.count() < self.max_usage


class Enrolement(models.Model):
    STATUS_CHOICES = (
        (0, "failed"),
        (1, "Success"),
        (2, "Canceled"),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrolements")
    enroled_at = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrolements")
    payment = models.OneToOneField(Payment, on_delete=models.SET_NULL, null=True, related_name="enrolement")
    total_amount = models.FloatField(default=0)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, related_name="enrolements")
    status = models.PositiveIntegerField(default=0, choices=STATUS_CHOICES)


class Review(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="reviews")
    profession = models.CharField(max_length=200, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name="reviews")

    def __str__(self) -> str:
        return self.user.get_full_name()

class Certifications(models.Model):
    pass


class Room(models.Model):
    name = models.TextField()
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_rooms")
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="messages")
    room = models.ForeignKey(
        Room, on_delete=models.SET_NULL, null=True, related_name="messages")
    body = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    reply_to = models.OneToOneField(
        "Message", on_delete=models.SET_NULL, null=True, related_name="replies")


class Question(models.Model):
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="questions")
    module = models.ForeignKey(
        Module, on_delete=models.SET_NULL, null=True, related_name="questions")
    created_at = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers")
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
