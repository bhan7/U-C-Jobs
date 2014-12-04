from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from models import *

class JobSeekerRegisterForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=100)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    birthdate = forms.DateField(input_formats=['%m/%d/%Y',],
                                widget=forms.DateInput(format='%m/%d/%Y'))
    password1 = forms.CharField(max_length=50, 
                                label='Password', 
                                widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=50, 
                                label='Confirm password',  
                                widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(JobSeekerRegisterForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("Email is already taken.")
        return email

class CompanyRegisterForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=100)
    company_name = forms.CharField(max_length=100)
    logo = forms.FileInput()
    password1 = forms.CharField(max_length=50, 
                                label='Password', 
                                widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=50, 
                                label='Confirm password',  
                                widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(CompanyRegisterForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("Email is already taken.")
        return email

class CompanyPostForm(forms.ModelForm):
    class Meta:
        model = CompanyPost
        exclude = ('user', 'post_time', 'follow_list', )

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        exclude = ('user', 'profile_type_is_company', 'verification', )
        widgets = {
            'photo' : forms.FileInput(),
            'logo' : forms.FileInput()
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class JobSeekerProfileForm(forms.ModelForm):
    graduation_date = forms.DateField(input_formats=['%m/%d/%Y',],
                                      widget=forms.DateInput(format='%m/%d/%Y'))
    class Meta:
        model = JobSeekerProfile
        exclude = ('user', 'profile_type_is_company', 'birthdate', )
        widgets = {
            'photo' : forms.FileInput(),
            'resume' : forms.FileInput()
        }

class EducationForm(forms.ModelForm):
    begin = forms.DateField(input_formats=['%m/%d/%Y',],
                            widget=forms.DateInput(format='%m/%d/%Y'))
    end = forms.DateField(input_formats=['%m/%d/%Y',],
                            widget=forms.DateInput(format='%m/%d/%Y'))
    class Meta:
        model = Education
        exclude = ('user',)

class WorkExpForm(forms.ModelForm):
    begin = forms.DateField(input_formats=['%m/%d/%Y',],
                            widget=forms.DateInput(format='%m/%d/%Y'))
    end = forms.DateField(input_formats=['%m/%d/%Y',],
                            widget=forms.DateInput(format='%m/%d/%Y'))
    class Meta:
        model = WorkExp
        exclude = ('user',)

class MailForm(forms.Form):
    receiver = forms.CharField(max_length=50)
    mail_subject = forms.CharField(max_length=100)
    mail_content = forms.CharField(max_length=5000)

    def clean(self):
        cleaned_data = super(MailForm, self).clean()
        return cleaned_data

    def clean_receiver(self):
        receiver = self.cleaned_data.get('receiver')
        if not User.objects.filter(username__exact=receiver):
            raise forms.ValidationError("User not exists.")
        return receiver

class SearchCompanyForm(forms.Form):
    location = forms.CharField(max_length=50, required=False)
    company_type = forms.CharField(max_length=50, required=False)
    company_name = forms.CharField(max_length=50, required=False)

class SearchJobSeekerForm(forms.Form):
    major = forms.CharField(max_length=50, required=False)
    school = forms.CharField(max_length=50, required=False)
    current_place = forms.CharField(max_length=50, required=False)
    graduation_date = forms.CharField(max_length=50, required=False)

class ResetPasswordForm(forms.Form):
    username = forms.CharField(max_length = 50)
    password_pre = forms.CharField(max_length = 50, 
                                label='Previous Password', 
                                widget = forms.PasswordInput())
    password1 = forms.CharField(max_length = 50, 
                                label='New Password', 
                                widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 50, 
                                label='Confirm New Password',  
                                widget = forms.PasswordInput())

    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords unmatch.")
        return cleaned_data

    def clean_password_pre(self):
        username = self.cleaned_data.get('username')
        password_pre = self.cleaned_data.get('password_pre')
        user = User.objects.get(username__exact=username)
        valid = user.check_password(password_pre)
        if not valid:
            raise forms.ValidationError("Password incorrect")
        return valid


