from django.urls import path

from . import views

app_name = 'sg'
urlpatterns = [
               path('', views.index, name='index'),
               path('writing/', views.writing, name='writing'),
               path('writing/save/', views.save, name='save'),
               path('writing/recommend/', views.recommend_words, name='recommend'),
               path('signup/', views.signup, name='signup'),
               path('login/', views.login, name='login'),
               path('logout/', views.logout, name='logout'),
               path('list/', views.list, name='list'),
               path('list/detail/<int:pk>/', views.detail, name='detail'),
               path('scrap/', views.scrap, name='scrap'),
               path('scraplist/', views.scraplist, name='scraplist')
               ]
