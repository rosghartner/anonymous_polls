from django.urls import path

from . import views

urlpatterns = [
    
    path('rating/', views.AddRatingViewSet.as_view({'post': 'create'}), name=''),
    path('poll-list/', views.PollsViewSet.as_view({'get': 'list'}), name='poll_list'),
    path('poll/<int:pk>', views.PollsViewSet.as_view({'get': 'retrieve'}), name='poll_id'),
    path('create-poll/', views.PollsViewSet.as_view({'post': 'create'}), name='create_poll'),
    path('update-poll/<int:pk>', views.PollsViewSet.as_view({'post': 'update'})),
    path('delete-poll/<int:pk>', views.PollsViewSet.as_view({'post': 'destroy'})),
    path('create-question/', views.QuestionsViewSet.as_view({'post': 'create'})),
    path('update-question/<int:pk>', views.QuestionsViewSet.as_view({'post': 'update'})),
    path('delete-question/<int:pk>', views.QuestionsViewSet.as_view({'post': 'destroy'})),
    path('create-answer/', views.AnswersViewSet.as_view({'post': 'create'})),
    path('update-answer/<int:pk>', views.AnswersViewSet.as_view({'post': 'update'})),
    path('delete-answer/<int:pk>', views.AnswersViewSet.as_view({'post': 'destroy'})),
    path('poll/choice', views.CreateChoiceViewSet.as_view({'post': 'create'})),
    path('poll/user-created', views.PollDataViewSet.as_view({'get': 'list'})),
    path('poll/data/<int:pk>', views.PollDataViewSet.as_view({'get': 'retrieve'})),
    path('user/polls/', views.ResultUserPollsViewSet.as_view({'get': 'list'})),
    path('user/polls/<int:pk>', views.ResultUserPollsViewSet.as_view({'get': 'retrieve'})),


]