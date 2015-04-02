from django.db import transaction
from django.http import HttpResponse, Http404, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import password_reset, password_reset_confirm
from mimetypes import guess_type
from ucjobs.forms import *
from ucjobs.models import *

# homepage
def home(request):
    if request.user.is_authenticated() == False:
        return HttpResponseRedirect(reverse('home_non_loggedin'))
    elif JobSeekerProfile.objects.filter(user=request.user):
        return HttpResponseRedirect(reverse('home_job_seeker'))
    else:
        return HttpResponseRedirect(reverse('home_company'))

def home_non_loggedin(request):
    context = {}

    context['company_profiles'] = CompanyProfile.objects.all()
    context['company_posts'] = CompanyPost.objects.all().order_by('id').reverse()
    
    return render(request, 'ucjobs/home-non-loggedin.html', context)

def get_company_logo(request, id):
    company_profile = get_object_or_404(CompanyProfile, id=id)
    if not company_profile.logo:
        raise Http404

    content_type = guess_type(company_profile.logo.name)
    return HttpResponse(company_profile.logo, content_type=content_type)

@login_required
def home_job_seeker(request):
    context = {}

    context['company_profiles'] = CompanyProfile.objects.all()
    context['company_posts'] = CompanyPost.objects.all().order_by('id').reverse()

    mail_unread = Mail.objects.filter(receiver=request.user).filter(read_status=False)
    context['mail_unread_number'] = str(mail_unread.count())
    
    return render(request, 'ucjobs/home-job-seeker.html', context)

@login_required
def home_company(request):
    context = {}

    context['company_profiles'] = CompanyProfile.objects.all()
    context['company_posts'] = CompanyPost.objects.all().order_by('id').reverse()

    mail_unread = Mail.objects.filter(receiver=request.user).filter(read_status=False)
    context['mail_unread_number'] = str(mail_unread.count())

    return render(request, 'ucjobs/home-company.html', context)


# register
@transaction.atomic
def job_seeker_register(request):
    context = {}
 
    if request.method == 'GET':
        context['form'] = JobSeekerRegisterForm()
        return render(request, 'ucjobs/job-seeker-register.html', context)
 
    form = JobSeekerRegisterForm(request.POST)
    context['form'] = form
     
    if not form.is_valid():
        return render(request, 'ucjobs/job-seeker-register.html', context)
 
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'], 
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'])
 
    # Mark the user as inactive to prevent login before email confirmation.
    new_user.is_active = False
    new_user.save()
 
    # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(new_user)
 
    # Initiate profile model
    new_job_seeker_profile = JobSeekerProfile(user=new_user, birthdate=form.cleaned_data['birthdate'])
    new_job_seeker_profile.save()
 
    email_body = """
    Welcome to U-C Jobs.  Please click the link below to
    verify your email address and complete the registration of your account:
 
    http://%s%s
    """ % (request.get_host(), 
     reverse('register_confirm', args=(new_user.username, token)))
 
    send_mail(subject="Verify your email address",
              message= email_body,
              from_email="ucjobswebsite@gmail.com",
              recipient_list=[new_user.email],
              fail_silently=False)

    context['email'] = form.cleaned_data['email']
 
    return render(request, 'ucjobs/register-confirm.html', context)
 
@transaction.atomic
def company_register(request):
    context = {}
 
    if request.method == 'GET':
        context['form'] = CompanyRegisterForm()
        return render(request, 'ucjobs/company-register.html', context)
 
    form = CompanyRegisterForm(request.POST, request.FILES)
    context['form'] = form
     
    if not form.is_valid():
        return render(request, 'ucjobs/company-register.html', context)
 
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['company_name'])
 
    # Mark the user as inactive to prevent login before email confirmation.
    new_user.is_active = False
    new_user.save()
 
    # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(new_user)
 
    # Initiate profile model
    new_company_profile = CompanyProfile(user=new_user, company_name=form.cleaned_data['company_name'], logo=request.FILES['logo'])
    new_company_profile.save()
 
    email_body = """
    Welcome to U-C Jobs.  Please click the link below to
    verify your email address and complete the registration of your account:
 
    http://%s%s
    """ % (request.get_host(), 
     reverse('register_confirm', args=(new_user.username, token)))
 
    send_mail(subject="Verify your email address",
              message= email_body,
              from_email="ucjobswebsite@gmail.com",
              recipient_list=[new_user.email])
 
    context['email'] = form.cleaned_data['email']
 
    return render(request, 'ucjobs/register-confirm.html', context)

def register_confirm(request, username, token):
    user = get_object_or_404(User, username=username)
 
    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404
 
    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'ucjobs/register-complete.html', {})

# reset password
# Reference A: http://blog.xjtian.com/post/54552214875/built-in-password-reset-views-in-django
# Reference B: http://blog.montylounge.com/2009/07/12/django-forgot-password/
def reset(request):
    return password_reset(request, template_name='ucjobs/reset.html',
        email_template_name='ucjobs/reset_email.txt',
        subject_template_name='ucjobs/reset_subject.txt',
        post_reset_redirect=reverse('reset_done'))

def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='ucjobs/reset_confirm.html',
        uidb64=uidb64, token=token, post_reset_redirect=reverse('reset_complete'))

def reset_done(request):
    return render(request, 'ucjobs/reset_done.html')

def reset_complete(request):
    return render(request, 'ucjobs/reset_complete.html')

@login_required
def reset_password_job_seeker(request):
    context = {}

    if request.method == 'GET':
        return render(request, 'ucjobs/reset-password-job-seeker.html', {})

    form = ResetPasswordForm(request.POST)

    context['form'] = form
    
    if not form.is_valid():
        return render(request, 'ucjobs/reset-password-job-seeker.html', context)

    # reset password
    user = request.user
    user.set_password(request.POST['password1'])
    user.save()
    update_session_auth_hash(request, user)

    return redirect('/ucjobs/show_job_seeker_profile_self')

@login_required
def reset_password_company(request):
    context = {}

    if request.method == 'GET':
        return render(request, 'ucjobs/reset-password-company.html', {})

    form = ResetPasswordForm(request.POST)

    context['form'] = form
    
    if not form.is_valid():
        return render(request, 'ucjobs/reset-password-company.html', context)

    # reset password
    user = request.user
    user.set_password(request.POST['password1'])
    user.save()
    update_session_auth_hash(request, user)

    return redirect('/ucjobs/show_company_profile_self')


# company post
def show_company_post_non_loggedin(request, id):
    context = {}
    context['company_post'] = CompanyPost.objects.get(id=id)
    return render(request, 'ucjobs/show-company-post-non-loggedin.html', context)

@login_required
def show_company_post_job_seeker(request, id):
    context = {}
    context['company_post'] = CompanyPost.objects.get(id=id)
    return render(request, 'ucjobs/show-company-post-job-seeker.html', context)

@login_required
def show_company_post_company(request, id):
    context = {}
    context['company_post'] = CompanyPost.objects.get(id=id)
    return render(request, 'ucjobs/show-company-post-company.html', context)

@login_required
def show_company_post_self(request, id):
    context = {}
    context['company_post'] = CompanyPost.objects.get(id=id)
    return render(request, 'ucjobs/show-company-post-self.html', context)

@login_required
@transaction.atomic
def add_company_post(request):
    context = {}

    if request.method == 'GET':
        context['form'] = CompanyPostForm()
        return render(request, 'ucjobs/add-company-post.html', context)

    form = CompanyPostForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'ucjobs/add-company-post.html', context)

    new_company_post = CompanyPost(user=request.user,
                                   location=request.POST['location'],
                                   post_subject=request.POST['post_subject'],
                                   post_content=request.POST['post_content'],
                                   position_type=request.POST['position_type'])
    new_company_post.save()

    return redirect('/ucjobs/show_company_profile_self')

@login_required
@transaction.atomic
def edit_company_post(request, id):
    context = {}
    company_post_to_edit = get_object_or_404(CompanyPost, id=id)
    context['company_post'] = company_post_to_edit
    
    if request.method == 'GET':
        form = CompanyPostForm(instance=company_post_to_edit)
        context['form'] = form
        return render(request, 'ucjobs/edit-company-post.html', context)

    form = CompanyPostForm(request.POST, instance=company_post_to_edit)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'ucjobs/edit-company-post.html', context)
    form.save()

    return render(request, 'ucjobs/edit-company-post.html', context)

@login_required
@transaction.atomic
def delete_company_post(request, id):
    company_post_to_delete = CompanyPost.objects.get(id=id)
    company_post_to_delete.delete()

    return redirect('/ucjobs/show_company_profile_self')


# company profile
def show_company_profile_non_loggedin(request, id):
    context = {}

    company_profile = CompanyProfile.objects.get(id=id)
    context['company_profile'] = company_profile
    context['company_posts'] = CompanyPost.objects.filter(user=company_profile.user).order_by('id').reverse()

    return render(request, 'ucjobs/show-company-profile-non-loggedin.html', context)

def get_company_photo(request, id):
    company_profile = get_object_or_404(CompanyProfile, id=id)
    if not company_profile.photo:
        raise Http404

    content_type = guess_type(company_profile.photo.name)
    return HttpResponse(company_profile.photo, content_type=content_type)

@login_required
def show_company_profile_job_seeker(request, id):
    context = {}

    company_profile = CompanyProfile.objects.get(id=id)
    context['company_profile'] = company_profile
    context['company_posts'] = CompanyPost.objects.filter(user=company_profile.user).order_by('id').reverse()
    context['messages'] = Message.objects.filter(company_profile=company_profile)
    context['form'] = MessageForm()

    return render(request, 'ucjobs/show-company-profile-job-seeker.html', context)

@login_required
def show_company_profile_company(request, id):
    context = {}

    company_profile = CompanyProfile.objects.get(id=id)
    context['company_profile'] = company_profile
    context['company_posts'] = CompanyPost.objects.filter(user=company_profile.user).order_by('id').reverse()
    context['messages'] = Message.objects.filter(company_profile=company_profile)

    return render(request, 'ucjobs/show-company-profile-company.html', context)

@login_required
def show_company_profile_self(request):
    context = {}

    company_profile = CompanyProfile.objects.get(user=request.user)
    context['company_profile'] = company_profile
    context['company_posts'] = CompanyPost.objects.filter(user=request.user).order_by('id').reverse()
    context['messages'] = Message.objects.filter(company_profile=company_profile)
    context['form'] = MessageForm()

    return render(request, 'ucjobs/show-company-profile-self.html', context)

@login_required
@transaction.atomic
def edit_company_profile(request):
    context = {}
    company_profile_to_edit = get_object_or_404(CompanyProfile, user=request.user)
    context['company_profile'] = company_profile_to_edit
    
    if request.method == 'GET':
        form = CompanyProfileForm(instance=company_profile_to_edit)
        context['form'] = form
        return render(request, 'ucjobs/edit-company-profile.html', context)

    form = CompanyProfileForm(request.POST, request.FILES, instance=company_profile_to_edit)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'ucjobs/edit-company-profile.html', context)
    form.save()

    return render(request, 'ucjobs/edit-company-profile.html', context)


# job seeker profile
@login_required
def show_job_seeker_profile_job_seeker(request, id):
    context = {}

    job_seeker_profile = JobSeekerProfile.objects.get(user=User.objects.get(id=id))
    context['job_seeker_profile'] = job_seeker_profile
    context['educations'] = Education.objects.filter(user=job_seeker_profile.user)
    context['work_exps'] = WorkExp.objects.filter(user=job_seeker_profile.user)

    return render(request, 'ucjobs/show-job-seeker-profile-job-seeker.html', context)

@login_required
def show_job_seeker_profile_company(request, id):
    context = {}

    job_seeker_profile = JobSeekerProfile.objects.get(user=User.objects.get(id=id))
    context['job_seeker_profile'] = job_seeker_profile
    context['educations'] = Education.objects.filter(user=job_seeker_profile.user)
    context['work_exps'] = WorkExp.objects.filter(user=job_seeker_profile.user)

    return render(request, 'ucjobs/show-job-seeker-profile-company.html', context)

@login_required
def show_job_seeker_profile_self(request):
    context = {}

    job_seeker_profile = JobSeekerProfile.objects.get(user=request.user)
    context['job_seeker_profile'] = job_seeker_profile
    context['educations'] = Education.objects.filter(user=job_seeker_profile.user)
    context['work_exps'] = WorkExp.objects.filter(user=job_seeker_profile.user)

    context['education_form'] = EducationForm()
    context['work_exp_form'] = WorkExpForm()

    return render(request, 'ucjobs/show-job-seeker-profile-self.html', context)

@login_required
def get_job_seeker_photo(request, id):
    job_seeker_profile = get_object_or_404(JobSeekerProfile, id=id)
    if not job_seeker_profile.photo:
        raise Http404

    content_type = guess_type(job_seeker_profile.photo.name)
    return HttpResponse(job_seeker_profile.photo, content_type=content_type)

@login_required
@transaction.atomic
def edit_job_seeker_profile(request):
    context = {}
    job_seeker_profile_to_edit = get_object_or_404(JobSeekerProfile, user=request.user)
    context['job_seeker_profile'] = job_seeker_profile_to_edit
    
    if request.method == 'GET':
        form = JobSeekerProfileForm(instance=job_seeker_profile_to_edit)
        context['form'] = form
        return render(request, 'ucjobs/edit-job-seeker-profile.html', context)

    form = JobSeekerProfileForm(request.POST, request.FILES, instance=job_seeker_profile_to_edit)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'ucjobs/edit-job-seeker-profile.html', context)
    form.save()

    return render(request, 'ucjobs/edit-job-seeker-profile.html', context)

@login_required
@transaction.atomic
def add_education(request):
    context = {}

    job_seeker_profile = JobSeekerProfile.objects.get(user=request.user)
    context['job_seeker_profile'] = job_seeker_profile
    context['educations'] = Education.objects.filter(user=job_seeker_profile.user)
    context['work_exps'] = WorkExp.objects.filter(user=job_seeker_profile.user)

    context['work_exp_form'] = WorkExpForm()

    education_form = EducationForm(request.POST)
    context['education_form'] = education_form

    if not education_form.is_valid():
        return render(request, 'ucjobs/show-job-seeker-profile-self.html', context)

    
    education = education_form.save(commit=False)
    education.user = request.user
    education.save()

    return redirect('/ucjobs/show_job_seeker_profile_self')

@login_required
@transaction.atomic
def edit_education(request, id):
    context = {}
    education_to_edit = get_object_or_404(Education, id=id)
    context['education'] = education_to_edit
    
    if request.method == 'GET':
        form = EducationForm(instance=education_to_edit)
        context['form'] = form
        return render(request, 'ucjobs/edit-education.html', context)

    form = EducationForm(request.POST, instance=education_to_edit)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'ucjobs/edit-education.html', context)
    form.save()

    return render(request, 'ucjobs/edit-education.html', context)

@login_required
@transaction.atomic
def delete_education(request, id):
    education_to_delete = Education.objects.get(id=id)
    education_to_delete.delete()

    return redirect('/ucjobs/show_job_seeker_profile_self')

@login_required
@transaction.atomic
def add_work_exp(request):
    context = {}

    job_seeker_profile = JobSeekerProfile.objects.get(user=request.user)
    context['job_seeker_profile'] = job_seeker_profile
    context['educations'] = Education.objects.filter(user=job_seeker_profile.user)
    context['work_exps'] = WorkExp.objects.filter(user=job_seeker_profile.user)

    context['education_form'] = EducationForm()

    work_exp_form = WorkExpForm(request.POST)
    context['work_exp_form'] = work_exp_form

    if not work_exp_form.is_valid():
        return render(request, 'ucjobs/show-job-seeker-profile-self.html', context)

    work_exp = work_exp_form.save(commit=False)
    work_exp.user = request.user
    work_exp.save()

    return redirect('/ucjobs/show_job_seeker_profile_self')

@login_required
@transaction.atomic
def edit_work_exp(request, id):
    context = {}
    work_exp_to_edit = get_object_or_404(WorkExp, id=id)
    context['work_exp'] = work_exp_to_edit
    
    if request.method == 'GET':
        form = WorkExpForm(instance=work_exp_to_edit)
        context['form'] = form
        return render(request, 'ucjobs/edit-work-exp.html', context)

    form = WorkExpForm(request.POST, instance=work_exp_to_edit)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'ucjobs/edit-work-exp.html', context)
    form.save()

    return render(request, 'ucjobs/edit-work-exp.html', context)

@login_required
@transaction.atomic
def delete_work_exp(request, id):
    work_exp_to_delete = WorkExp.objects.get(id=id)
    work_exp_to_delete.delete()

    return redirect('/ucjobs/show_job_seeker_profile_self')

# job seeker mail box
@login_required
def job_seeker_mail_inbox(request):
    context = {}

    context['mail_inbox'] = Mail.objects.filter(receiver=request.user).order_by('id').reverse()

    return render(request, 'ucjobs/job-seeker-mail-inbox.html', context)

@login_required
def job_seeker_mail_sent(request):
    context = {}

    context['mail_sent'] = Mail.objects.filter(sender=request.user).order_by('id').reverse()

    return render(request, 'ucjobs/job-seeker-mail-sent.html', context)

@login_required
def job_seeker_mail_compose(request):
    context = {}

    if request.method == 'GET':
        context['form'] = MailForm()
        return render(request, 'ucjobs/job-seeker-mail-compose.html', context)

    form = MailForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'ucjobs/job-seeker-mail-compose.html', context)

    new_mail = Mail(sender=request.user,
                    receiver=User.objects.get(username=request.POST['receiver']),
                    mail_subject=request.POST['mail_subject'],
                    mail_content=request.POST['mail_content'])
    new_mail.save()

    return redirect('/ucjobs/job_seeker_mail_inbox')

@login_required
def job_seeker_mail_read(request, id):
    context = {}

    mail = Mail.objects.get(id=id)
    mail.read_status = True
    mail.save()
    context['mail'] = mail

    return render(request, 'ucjobs/job-seeker-mail-read.html', context)


# company mail box
@login_required
def company_mail_inbox(request):
    context = {}

    context['mail_inbox'] = Mail.objects.filter(receiver=request.user).order_by('id').reverse()

    return render(request, 'ucjobs/company-mail-inbox.html', context)

@login_required
def company_mail_sent(request):
    context = {}

    context['mail_sent'] = Mail.objects.filter(sender=request.user).order_by('id').reverse()

    return render(request, 'ucjobs/company-mail-sent.html', context)

@login_required
@transaction.atomic
def company_mail_compose(request):
    context = {}

    if request.method == 'GET':
        context['form'] = MailForm()
        return render(request, 'ucjobs/company-mail-compose.html', context)

    form = MailForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'ucjobs/company-mail-compose.html', context)

    new_mail = Mail(sender=request.user,
                    receiver=User.objects.get(username=request.POST['receiver']),
                    mail_subject=request.POST['mail_subject'],
                    mail_content=request.POST['mail_content'])
    new_mail.save()

    return redirect('/ucjobs/company_mail_sent')

@login_required
def company_mail_read(request, id):
    context = {}

    mail = Mail.objects.get(id=id)
    mail.read_status = True
    mail.save()
    context['mail'] = mail

    return render(request, 'ucjobs/company-mail-read.html', context)


# search
@login_required
def search_job_seeker(request):
    context = {}
    context['form'] = SearchJobSeekerForm()
    return render(request, 'ucjobs/search-job-seeker.html', context)

@login_required
def search_company(request):
    context = {}
    context['form'] = SearchCompanyForm()
    return render(request, 'ucjobs/search-company.html', context)


# functions for js & Ajax
@login_required
def reload_mail_unread_number(request):
    mail_unread = Mail.objects.filter(receiver=request.user).filter(read_status=False)
    mail_unread_number = str(mail_unread.count())

    # Ajax
    response_text = mail_unread_number
    return HttpResponse(response_text)

@login_required
@transaction.atomic
def search_job_seeker_result(request):
    context = {}

    form = SearchJobSeekerForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'ucjobs/search-job-seeker.html', context)

    major = request.POST['major']
    school = request.POST['school']
    current_place = request.POST['current_place']

    if school == '' and major == '':
        if current_place == '':
            context['result'] = []
        else:
            context['result'] = JobSeekerProfile.objects.filter(current_place__contains=current_place)
    else:
        user_ids = Education.objects.filter(school__contains=school).filter(major__contains=major).values_list('user_id', flat=True)
        users = User.objects.filter(id__in=user_ids)
        context['result'] = JobSeekerProfile.objects.filter(user__in=users).filter(current_place__contains=current_place)

    print context['result']
    return render(request, 'ucjobs/search-job-seeker-result.html', context)

@login_required
@transaction.atomic
def search_company_result(request):
    context = {}

    form = SearchCompanyForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'ucjobs/search-company.html', context)

    location = request.POST['location']
    company_type = request.POST['company_type']
    company_name = request.POST['company_name']

    if location != '' or company_type != '' or company_name != '':
        context['result'] = CompanyProfile.objects.filter(location__contains=location).filter(company_type__contains=company_type).filter(company_name__contains=company_name)

    return render(request, 'ucjobs/search-company-result.html', context)

@login_required
@transaction.atomic
def interest_company_post(request, id):
    context = {}

    company_post = CompanyPost.objects.get(id=id)

    if company_post.follow_list.filter(id=request.user.id).exists():
        company_post.follow_list.remove(request.user)
    else:
        company_post.follow_list.add(request.user)
        company_post.save()

    context['company_post'] = company_post

    return render(request, 'ucjobs/interest-post.html', context)

@login_required
@transaction.atomic
def add_message_job_seeker(request, id):
    context = {}

    company_profile = CompanyProfile.objects.get(id=id)
    context['company_profile'] = company_profile
    context['messages'] = Message.objects.filter(company_profile=company_profile)

    form = MessageForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'ucjobs/add-message-job-seeker.html', context)

    new_message = Message(user=request.user,
                          content=request.POST['content'],
                          company_profile=company_profile)
    new_message.save()

    context['messages'] = Message.objects.filter(company_profile=company_profile)

    return render(request, 'ucjobs/add-message-job-seeker.html', context)

@login_required
@transaction.atomic
def add_message_self(request, id):
    context = {}

    company_profile = CompanyProfile.objects.get(id=id)
    context['company_profile'] = company_profile
    context['messages'] = Message.objects.filter(company_profile=company_profile)

    form = MessageForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'ucjobs/add-message-self.html', context)

    new_message = Message(user=request.user,
                          content=request.POST['content'],
                          company_profile=company_profile)
    new_message.save()

    context['messages'] = Message.objects.filter(company_profile=company_profile)

    return render(request, 'ucjobs/add-message-self.html', context)



