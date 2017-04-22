from django.conf.urls import url

from . import views

app_name = 'reviewer'
urlpatterns = [
    # index with all the cards and the user-specific study-progress
    url(r'^index$', views.IndexView.as_view(), name='index'),
    # detail view of each card
    url(r'^card/(?P<pk>[0-9]+)/$', views.CardDetail.as_view(), name='card_detail'),
    # List of all the Cards of one user
    url(r'^user/([\w-]+)/cardlist/$', views.UserCardList.as_view(), name='user_cardlist'),
    # user_profile is gotten either through username or id
    url(r'^user/(?P<slug>[\w.@+-]+)/$', views.UserProfile.as_view(), name='user_profile_name'),
    url(r'^id/(?P<pk>[0-9]+)/$', views.UserProfile.as_view(), name='user_profile_id'),


    # view for the actual studying
    #url(r'^$', views.)

]
