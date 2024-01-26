from django import forms
from typing import Any
from contact.models import Contact
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
            }
        )
    )

    class Meta:
        model = Contact
        fields = (
            'first_name', 'last_name', 'phone',
            'email', 'description', 'category',
            'picture', 'owner',
        )

    def clean(self) -> dict[str, Any]:
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name == last_name:
            self.add_error(
                'last_name',
                ValidationError(
                    'Primeiro nome não pode ser igual ao segundo',
                    code='invalid',
                )
            )
        return super().clean()

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name == 'ABC':
            self.add_error(
                'first_name',
                ValidationError(
                    'Não pode ser ABC',
                    code='invalid'
                )
            )
        return first_name


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2',
        )

    def clean_email(self):
        data = self.cleaned_data.get('email')

        if User.objects.filter(email=data).exists():
            self.add_error(
                'email',
                ValidationError(
                    'Este e-mail já está sendo usado', code='invalid'
                )
            )
        return data


class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Please, add more than 2 letters.'
        }
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.'
    )
    password1 = forms.CharField(
        label='Password 1',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )
    password2 = forms.CharField(
        label='Password 2',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='Use the same password as before.',
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username',
        )

    def clean_email(self):
        data = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != data:
            if User.objects.filter(email=data).exists():
                self.add_error(
                    'email',
                    ValidationError(
                        'Este e-mail já está sendo usado', code='invalid'
                    )
                )
        return data

    def save(self, commit: bool = True):
        cleanded_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleanded_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self) -> dict[str, Any]:
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('As senhas são diferentes', code='invalid')
                )
        return super().clean()

    def clean_password1(self):
        data = self.cleaned_data.get("password1")

        if data:
            try:
                password_validation.validate_password(data)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors),
                )
        return data
