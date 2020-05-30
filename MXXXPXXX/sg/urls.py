from django.urls import path

from . import views

app_name = 'sg'
urlpatterns = [
    path('', views.index, name='index'),
    path('writing/', views.writing, name='writing'),
    path('signup/',views.signup,name='signup')
]