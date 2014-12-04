from django.db import models
from django.contrib.auth.models import User

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User)
    gender = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    id_number = models.CharField(max_length=50, blank=True)
    birthdate = models.DateField(auto_now_add=False)
    birthplace = models.CharField(max_length=50, blank=True)
    current_place = models.CharField(max_length=50, blank=True)
    politics_status = models.CharField(max_length=50, blank=True)
    graduation_date = models.DateField(auto_now_add=False, null=True)
    description = models.CharField(max_length=5000, blank=True)
    photo = models.ImageField(upload_to="jobseeker_photos", blank=True)
    resume = models.FileField(upload_to="jobseeker_resumes", blank=True)
    def __unicode__(self):
        return self.id_number

class Education(models.Model):
    user = models.ForeignKey(User)
    begin = models.DateField(auto_now_add=False)
    end = models.DateField(auto_now_add=False)
    school = models.CharField(max_length=50)
    degree = models.CharField(max_length=50)
    major = models.CharField(max_length=50)
    def __unicode__(self):
        return self.school + self.id

class WorkExp(models.Model):
    user = models.ForeignKey(User)
    begin = models.DateField(auto_now_add=False)
    end = models.DateField(auto_now_add=False)
    company = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    description = models.CharField(max_length=5000)
    def __unicode__(self):
        return self.company + self.id

class CompanyProfile(models.Model):
    user = models.OneToOneField(User)
    company_name = models.CharField(max_length=50)
    company_website = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=50, blank=True)
    company_type = models.CharField(max_length=50, blank=True)
    employee_num = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=5000, blank=True)
    photo = models.ImageField(upload_to="company_photos", blank=True)
    logo = models.ImageField(upload_to="company_logos", blank=True)
    def __unicode__(self):
        return self.company_name

class Message(models.Model):
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=200)
    company_profile = models.ForeignKey(CompanyProfile)
    def __unicode__(self):
        return self.content + self.id

class Mail(models.Model):
    sender = models.ForeignKey(User, related_name='sender')
    receiver = models.ForeignKey(User, related_name='receiver')
    mail_time = models.DateTimeField(auto_now_add=True)
    mail_subject = models.CharField(max_length=100)
    mail_content = models.CharField(max_length=5000)
    read_status = models.BooleanField(default=False)
    def __unicode__(self):
        return self.mail_subject + self.id

class CompanyPost(models.Model):
    user = models.ForeignKey(User)
    location = models.CharField(max_length=50)
    post_time = models.DateTimeField(auto_now_add=True)
    post_subject = models.CharField(max_length=100)
    post_content = models.CharField(max_length=5000)
    position_type = models.CharField(max_length=50)
    follow_list = models.ManyToManyField(User, related_name='followList', blank=True)
    def __unicode__(self):
        return self.post_subject + self.id