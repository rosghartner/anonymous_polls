from django.urls import path

from . import views

urlpatterns = [
    path('poll/', views.PollListView.as_view()),
    path('poll/<int:pk>', views.PollDetailView.as_view()),
    path('poll/create', views.CreateNewPollView.as_view()),
    path('poll/update/<int:pk>', views.UpdatePollView.as_view()),
    path('rating/', views.AddRatingView.as_view()),
]