from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

app_name = 'reviewer'
urlpatterns = [
    # base-page
    url(r'^$', views.home, name='home'),
    # index with all the cards and the user-specific study-progress
    url(r'^index/$', views.IndexView.as_view(), name='index'),
    # detail view of each card
    url(r'^card/(?P<pk>[0-9]+)/$', views.CardDetail.as_view(), name='card_detail'),
    # List of all the Cards of one user
    url(r'^user/([\w-]+)/cardlist/$', views.UserCardList.as_view(), name='user_cardlist'),
    # user_profile is gotten either through username or id
    url(r'^user/(?P<slug>[\w.@+-]+)/$', views.UserProfile, name='user_profile_name'),
    url(r'^id/(?P<pk>[0-9]+)/$', views.UserProfile, name='user_profile_id'),


    # views for the actual studying
    url(r'^study_start/(?P<name>.+)/(?P<setting>[\w-]+)/$', views.study_start, name='study_start'),
    url(r'^studying/(?P<pk>[0-9]+)/$', views.studying, name='studying'),
    url(r'^studying_finished/$', views.studying_finished, name='studying_finished'),

    url(r'^button/(?P<button>[0-9])/(?P<pk>[0-9]+)/$', views.button, name='button'),

    # views for the case_programm
    url(r'^case_creation/(?P<area>[\w-]+)/$', views.case_creation, name='case_creation'),
    url(r'^case_edit/(?P<area>[\w-]+)/(?P<pk>[0-9]+)/$', views.case_edit, name='case_edit'),
    url(r'^case_reviewer/(?P<area>[\w-]+)/(?P<pk>[0-9]+)/$', views.case_reviewer, name='case_reviewer'),
    url(r'^case_finished/(?P<area>[\w-]+)/(?P<pk>[0-9]+)/$', views.case_finished, name='case_finished'),

    #
    url(r'^contact/$', views.contact, name='contact'),















# Account related urls and included views

    # for sign up with email-verification
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),

    # for login default is in 'registration/login.html'
    url(r'^login/$', auth_views.login, name='login'),
    # for logout, needs context so it doesn't go to 'registration/logout.html'
    url(r'^logout/$', auth_views.logout, {'next_page': 'reviewer:home' }, name='logout'),

    # for passwort reset via email (email.backend in settings.py):
    # the passwort reset confirm view tries to render the original template from auth, so changed to passwort_reset_email1.html; needs also next view and view as context b/c it uses default:
    url(r'^password_reset/$', auth_views.password_reset, {'post_reset_redirect' : 'reviewer:password_reset_done', 'email_template_name' : 'registration/password_reset_email1.html', 'template_name' : 'registration/password_reset_form1.html'}, name='password_reset'),
    url(r'^password_reset_done/$', auth_views.password_reset_done, {'template_name' : 'registration/password_reset_done1.html'}, name='password_reset_done'),
    # needs the next view as sepcially named context, b/c uses default
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, {'post_reset_redirect' : 'reviewer:password_reset_complete', 'template_name' : 'registration/password_reset_complete1.html'}, name='password_reset_confirm'),
        # tries to render default, so renamed
    url(r'^reset/done/$', auth_views.password_reset_complete, {'template_name' : 'registration/password_reset_complete1.html'}, name='password_reset_complete'),

    #change password
    url(r'^password/$', views.change_password, name='change_password'),



]
