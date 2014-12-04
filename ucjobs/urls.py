from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # homepage
    url(r'^$', 'ucjobs.views.home', name='home'),
    url(r'^home_non_loggedin$', 'ucjobs.views.home_non_loggedin', name='home_non_loggedin'),
    url(r'^home_job_seeker$', 'ucjobs.views.home_job_seeker', name='home_job_seeker'),
    url(r'^home_company$', 'ucjobs.views.home_company', name='home_company'),    
    url(r'^get_company_logo/(?P<id>\d+)$', 'ucjobs.views.get_company_logo', name='get_company_logo'),

    # login and logout
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'ucjobs/login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),

    # register
    url(r'^job_seeker_register$', 'ucjobs.views.job_seeker_register', name='job_seeker_register'),
    url(r'^company_register$', 'ucjobs.views.company_register', name='company_register'),
    url(r'^register_confirm/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'ucjobs.views.register_confirm', name='register_confirm'),

    # reset password
    url(r'^reset$', 'ucjobs.views.reset', name='reset'),
    url(r'^reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'ucjobs.views.reset_confirm', name='reset_confirm'),
    url(r'^reset_complete$', 'ucjobs.views.reset_complete', name='reset_complete'),
    url(r'^reset_done$', 'ucjobs.views.reset_done', name='reset_done'),
    url(r'^reset_password_job_seeker$', 'ucjobs.views.reset_password_job_seeker', name='reset_password_job_seeker'),
    url(r'^reset_password_company$', 'ucjobs.views.reset_password_company', name='reset_password_company'),

    # company post
    url(r'^show_company_post_non_loggedin/(?P<id>\d+)$', 'ucjobs.views.show_company_post_non_loggedin', name='show_company_post_non_loggedin'),
    url(r'^show_company_post_job_seeker/(?P<id>\d+)$', 'ucjobs.views.show_company_post_job_seeker', name='show_company_post_job_seeker'),
    url(r'^show_company_post_company/(?P<id>\d+)$', 'ucjobs.views.show_company_post_company', name='show_company_post_company'),
    url(r'^show_company_post_self/(?P<id>\d+)$', 'ucjobs.views.show_company_post_self', name='show_company_post_self'),
    url(r'^add_company_post$', 'ucjobs.views.add_company_post', name='add_company_post'),
    url(r'^edit_company_post/(?P<id>\d+)$', 'ucjobs.views.edit_company_post', name='edit_company_post'),
    url(r'^delete_company_post/(?P<id>\d+)$', 'ucjobs.views.delete_company_post', name='delete_company_post'), 
    url(r'^interest_company_post/(?P<id>\d+)$', 'ucjobs.views.interest_company_post', name='interest_company_post'),

    # company profile
    url(r'^show_company_profile_non_loggedin/(?P<id>\d+)$', 'ucjobs.views.show_company_profile_non_loggedin', name='show_company_profile_non_loggedin'),
    url(r'^show_company_profile_job_seeker/(?P<id>\d+)$', 'ucjobs.views.show_company_profile_job_seeker', name='show_company_profile_job_seeker'),
    url(r'^show_company_profile_company/(?P<id>\d+)$', 'ucjobs.views.show_company_profile_company', name='show_company_profile_company'),
    url(r'^show_company_profile_self$', 'ucjobs.views.show_company_profile_self', name='show_company_profile_self'),
    url(r'^get_company_photo/(?P<id>\d+)$', 'ucjobs.views.get_company_photo', name='get_company_photo'),
    url(r'^edit_company_profile$', 'ucjobs.views.edit_company_profile', name='edit_company_profile'),
    url(r'^add_message_job_seeker/(?P<id>\d+)$', 'ucjobs.views.add_message_job_seeker', name='add_message_job_seeker'),
    url(r'^add_message_self/(?P<id>\d+)$', 'ucjobs.views.add_message_self', name='add_message_self'),

    # job seeker profile
    url(r'^show_job_seeker_profile_job_seeker/(?P<id>\d+)$', 'ucjobs.views.show_job_seeker_profile_job_seeker', name='show_job_seeker_profile_job_seeker'),
    url(r'^show_job_seeker_profile_company/(?P<id>\d+)$', 'ucjobs.views.show_job_seeker_profile_company', name='show_job_seeker_profile_company'),
    url(r'^show_job_seeker_profile_self$', 'ucjobs.views.show_job_seeker_profile_self', name='show_job_seeker_profile_self'),
    url(r'^get_job_seeker_photo/(?P<id>\d+)$', 'ucjobs.views.get_job_seeker_photo', name='get_job_seeker_photo'),
    url(r'^edit_job_seeker_profile$', 'ucjobs.views.edit_job_seeker_profile', name='edit_job_seeker_profile'),
    url(r'^add_education$', 'ucjobs.views.add_education', name='add_education'),
    url(r'^edit_education/(?P<id>\d+)$', 'ucjobs.views.edit_education', name='edit_education'),
    url(r'^delete_education/(?P<id>\d+)$', 'ucjobs.views.delete_education', name='delete_education'),
    url(r'^add_work_exp$', 'ucjobs.views.add_work_exp', name='add_work_exp'),
    url(r'^edit_work_exp/(?P<id>\d+)$', 'ucjobs.views.edit_work_exp', name='edit_work_exp'),
    url(r'^delete_work_exp/(?P<id>\d+)$', 'ucjobs.views.delete_work_exp', name='delete_work_exp'),

    # job seeker mail
    url(r'^job_seeker_mail_inbox$', 'ucjobs.views.job_seeker_mail_inbox', name='job_seeker_mail_inbox'),
    url(r'^job_seeker_mail_sent$', 'ucjobs.views.job_seeker_mail_sent', name='job_seeker_mail_sent'),
    url(r'^job_seeker_mail_compose$', 'ucjobs.views.job_seeker_mail_compose', name='job_seeker_mail_compose'),
    url(r'^job_seeker_mail_read/(?P<id>\d+)$', 'ucjobs.views.job_seeker_mail_read', name='job_seeker_mail_read'),

    # company mail
    url(r'^company_mail_inbox$', 'ucjobs.views.company_mail_inbox', name='company_mail_inbox'),
    url(r'^company_mail_sent$', 'ucjobs.views.company_mail_sent', name='company_mail_sent'),
    url(r'^company_mail_compose$', 'ucjobs.views.company_mail_compose', name='company_mail_compose'),
    url(r'^company_mail_read/(?P<id>\d+)$', 'ucjobs.views.company_mail_read', name='company_mail_read'),

    # search
    url(r'^search_job_seeker$', 'ucjobs.views.search_job_seeker', name='search_job_seeker'),
    url(r'^search_company$', 'ucjobs.views.search_company', name='search_company'),

    # functions for js & Ajax
    url(r'^reload_mail_unread_number$', 'ucjobs.views.reload_mail_unread_number', name='reload_mail_unread_number'),
    url(r'^search_job_seeker_result$', 'ucjobs.views.search_job_seeker_result', name='search_job_seeker_result'),
    url(r'^search_company_result$', 'ucjobs.views.search_company_result', name='search_company_result'),
)
