from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        clean_data = super().clean()
        password = clean_data["password"]
        confirm_password = clean_data["confirm_password"]

        if password != confirm_password:
            raise forms.ValidationError("Password entered are not same!")

        if len(password) < 8:
            raise forms.ValidationError("Password is too short!")

        if len(password) > 15:
            raise forms.ValidationError("Password is too long!")

        nums = [str(i) for i in range(10)]

        number, lower, upper, special = False, False, False, False

        for p in password:
            if p in nums:
                number = True
            if 0 <= ord(p) - 65 <= 25:
                upper = True
            if 0 <= ord(p) - 97 <= 25:
                lower = True
            if p in ['@', '#', '&']:
                special = True

        if not (number and lower and upper and special):
            raise forms.ValidationError("Password invalid")

    class Meta:
        model = User
        fields = ('email', 'about', 'gender', 'avatar', 'password', 'name')


class UpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('name', 'about', 'avatar')
