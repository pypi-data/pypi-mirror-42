from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name='nicha'
urlpatterns=[
    url(r'^$', views.index,name='Index'),
    url(r'^faq/$', views.faq,name='FAQ'),
    url(r'^mobile/$', views.mobile,name='Mobile'),
    url(r'^terms/$', views.terms_and_conditions,name='TermsAndConditions'),
    url(r'^privacy/$', views.privacy_policy,name='PrivacyPolicy'),
    url(r'^how-it-works/$', views.how_it_works,name='howItWorks'),
    url(r'^community/$', views.community,name='Community'),
    url(r'^account/$', views.account,name='Account'),
    url(r'^accounts/login/$', views.sign_in_to_account, name='SignInToAnAccount'),
    url(r'^accounts/logout/$',view.sign_out, name='Logout'),
    url(r'^accounts/create/$',view.create_account, name='CreateNewAccount'),
    path('accounts/password-change/',
        auth_views.PasswordChangeView.as_view(template_name='nicha/change_password.html'),
    ),
    path('accounts/password-reset/',
        auth_views.PasswordChangeView.as_view(template_name='nicha/password_reset.html'),
    ),

]
