from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import Flat
from .models import CustomUser, Role

class BaseSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone')

class SecretarySignUpForm(BaseSignUpForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = Role.SECRETARY
        if commit:
            user.save()
        return user

class ResidentSignUpForm(BaseSignUpForm):
    flat = forms.ModelChoiceField(
        queryset=Flat.objects.all(), 
        required=True, 
        help_text="Select your Flat"
    )

    class Meta(BaseSignUpForm.Meta):
        fields = BaseSignUpForm.Meta.fields + ('flat',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = Role.RESIDENT
        user.flat = self.cleaned_data.get('flat')
        if commit:
            user.save()
        return user

class GuardSignUpForm(BaseSignUpForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = Role.SECURITY
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'profile_photo')
