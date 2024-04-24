from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django import forms
from users.models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'mobile_number', "first_name",
                  "last_name", "gender", "tutor")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('password', 'first_name', 'last_name', 'tutor', 'is_active',
                  'admin', 'staff', 'mobile_number')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        "first_name",
        "last_name",
        "email",
        "mobile_number",
        "gender",
        "admin",
        "staff",
        "is_active",
        "tutor",
        "profile_picture",
    ]

    list_display_links = [
        "email"
    ]

    list_filter = []

    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',
         'mobile_number', 'gender', 'profile_picture')}),
        ('Permissions', {
         'fields': ('admin', 'staff', 'is_active', 'tutor')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name',
                       'mobile_number', 'gender', 'profile_picture', 'tutor', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'mobile_number', 'first_name', 'last_name')
    ordering = ('email', 'added_on',)
    filter_horizontal = ()
