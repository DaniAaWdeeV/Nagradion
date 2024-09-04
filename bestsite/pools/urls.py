from django.urls import path

from . import views

app_name = "pools"

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('time/', views.getTime, name='currentTime'),
    path('<int:pk>/', views.DetailView.as_view(), name='details'),
    path('<int:question_id>/vote', views.vote, name='vote'),
    path('<int:pk>/results', views.ResultsView.as_view(), name='results'),

]