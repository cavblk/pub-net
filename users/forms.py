from django import forms
from django.contrib.auth.password_validation import validate_password, password_validators_help_text_html
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

AuthUser = get_user_model()


# class RegisterForm(forms.Form):
#     first_name = forms.CharField(label='First name', max_length=255, required=True)
#     last_name = forms.CharField(label='Last name', max_length=255, required=True)
#     email = forms.EmailField(label='Email', max_length=255, required=True)
#     password = forms.CharField(
#         label='Password',
#         widget=forms.PasswordInput,
#         required=True,
#         help_text=password_validators_help_text_html()
#     )
#     password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=True)
#
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#
#         try:
#             AuthUser.objects.get(email=email)
#         except AuthUser.DoesNotExist:
#             return email
#         else:
#             raise forms.ValidationError('Email already taken.')
#
#     def clean_password(self):
#         first_name = self.cleaned_data.get('first_name')
#         last_name = self.cleaned_data.get('last_name')
#         email = self.cleaned_data.get('email')
#         password = self.cleaned_data.get('password')
#
#         user = AuthUser(
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#         )
#
#         validate_password(password, user)
#
#         return password
#
#     def clean_password_confirmation(self):
#         password = self.cleaned_data.get('password')
#         password_confirmation = self.cleaned_data.get('password_confirmation')
#
#         if password_confirmation != password:
#             raise forms.ValidationError('Password confirmation mismatch.')
#
#         return password_confirmation
#
#     def save(self):
#         first_name = self.cleaned_data.get('first_name')
#         last_name = self.cleaned_data.get('last_name')
#         email = self.cleaned_data.get('email')
#         password = self.cleaned_data.get('password')
#
#         user = AuthUser.objects.create_user(
#             username=email,
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             password=password,
#         )
#
#         return user

# Check django.contrib.auth.forms.UserCreationForm
class RegisterForm(forms.ModelForm):
    class Meta:
        model = AuthUser
        fields = ['first_name', 'last_name', 'email']

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        required=True,
        help_text=password_validators_help_text_html(),
    )

    password_confirmation = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
        required=True,
    )

    def clean_password(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        user = AuthUser(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        validate_password(password, user)

        return password

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        if password_confirmation != password:
            raise forms.ValidationError('Password confirmation mismatch.')

        return password_confirmation

    def save(self, commit=True):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        self.instance.username = email
        self.instance.set_password(password)

        return super().save(commit)
