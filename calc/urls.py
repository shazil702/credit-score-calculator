from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login_page, name='login'),
    path('submit-answers/', views.submit_answers, name='submit_answers'),
    path('score/', views.score_page, name='score_page'),
]