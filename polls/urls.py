from django.urls import path

from . import views

urlpatterns = [
    path('poll/choice', views.CreateChoiceViewSet.as_view({'post': 'create'})),
    #path('poll/update/<int:pk>', views.UpdatePollView.as_view()),

    path('rating/', views.AddRatingViewSet.as_view({'post': 'create'})), #works
    path('poll-list/', views.PollsViewSet.as_view({'get': 'list'})), #works
    path('poll/<int:pk>', views.PollsViewSet.as_view({'get': 'retrieve'})), #works
    path('create-poll/', views.PollsViewSet.as_view({'post': 'create'})), #works
    path('update-poll/<int:pk>', views.PollsViewSet.as_view({'post': 'update'})), #works
    path('delete-poll/<int:pk>', views.PollsViewSet.as_view({'post': 'destroy'})), #works
    path('create-question/', views.QuestionsViewSet.as_view({'post': 'create'})), #works
    path('update-question/<int:pk>', views.QuestionsViewSet.as_view({'post': 'update'})), #works
    path('delete-question/<int:pk>', views.QuestionsViewSet.as_view({'post': 'destroy'})), #works
    path('create-answer/', views.AnswersViewSet.as_view({'post': 'create'})), #works
    path('update-answer/<int:pk>', views.AnswersViewSet.as_view({'post': 'update'})), #works
    path('delete-answer/<int:pk>', views.AnswersViewSet.as_view({'post': 'destroy'})), #works
    path('poll/data/<int:pk>', views.PollDataViewSet.as_view({'get': 'retrieve'})),
    path('user/polls/', views.PollsViewSet.as_view({'get': 'retrieve'})),

]