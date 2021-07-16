from django.http import request
from rest_framework import permissions, generics, viewsets, mixins, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models
 
from .models import Poll, Question, Answer
from .serializers import (
    PollListSerializer, 
    PollDetailSerializer, 
    PollCreateSerializer,
    PollUpdateSerializer, 
    CreateRatingSerializer,
    CreateChoiceSerializer,
    AnswerSerializer,
    QuestionSerializer,
    QuestionCreateSerializer,
    QuestionUpdateSerializer,
    AnswerCreateSerializer)

class Round(models.Func): #функция для округления до десятых
    """Округление до десятых"""
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 1)'

class PollsViewSet(viewsets.ModelViewSet):
    """Вьюсет для опросов"""
    serializer_class = PollListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        polls = Poll.objects.annotate(
            rating_user = models.Count('ratings', filter=models.Q(ratings__user=self.request.user)) #проверяем голосовал ли пользователь
        ).annotate(
            middle_rate = Round(models.Avg("ratings__rate"))
        ).all()
        return polls

    def get_serializer_class(self):
        if self.action == 'list':
            return PollListSerializer
        elif self.action == "retrieve":
            return PollCreateSerializer
        elif self.action =='create':
            return PollCreateSerializer
        elif self.action =='update':
            return PollUpdateSerializer
        elif self.action =='destroy':
            return PollCreateSerializer

class AddRatingViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """добавление рейтинга опросу"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateRatingSerializer


class QuestionsViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    """Создание, удаление, обновление вопросов"""
    permission_classes = [permissions.IsAuthenticated]

    queryset = Question.objects.filter()

    def get_serializer_class(self):
        if self.action == 'create':
            return QuestionCreateSerializer
        elif self.action == "update":
            return QuestionUpdateSerializer
        elif self.action =='destroy':
            return QuestionUpdateSerializer


class AnswersViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    """Создание, удаление, обновление ответов"""
    permission_classes = [permissions.IsAuthenticated]
    queryset = Answer.objects.all()
    def get_serializer_class(self):
        if self.action == 'create':
            return AnswerCreateSerializer
        elif self.action == "update":
            return AnswerSerializer
        elif self.action =='destroy':
            return AnswerSerializer


class CreateChoiceViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """Сохранение результатов прохождения опроса"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateChoiceSerializer
    
    

class PollDataViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    """Данные об опросе"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PollDetailSerializer

    def get_queryset(self):
        poll = Poll.objects.annotate(

        ).filter()
        #return super().get_queryset()
        return poll


# def perform_create(self, serializer):
#     poll = serializer.save()
#     #poll = Poll.objects.create(**serializer.validated_data)
#     #print('************serial.validdata', serializer.validated_data)
#     poll_ = Poll.objects.get('?')
#     questions = serializer.validated_data.get('questions')
#     print(' o hi mark ********', questions)
#     Question.objects.bulk_create(
#         Question(poll = poll_, **question)
#         for question in questions
#     )
    
#     #return super().perform_create(serializer)
#     return poll


# class CreateNewPollView(generics.CreateAPIView): #переделать
#     """Создание нового опроса"""
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = PollCreateSerializer


# class UpdatePollView(generics.RetrieveUpdateAPIView):#переделать
#     """Редактирование Опроса"""
#     serializer_class = PollCreateSerializer
#     queryset = Poll.objects.all()



# class AddRatingView(generics.CreateAPIView):
#     """добавление рейтинга опросу"""
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = CreateRatingSerializer


# class PollListView(generics.ListAPIView):
#     """вывод списка опросов"""
#     serializer_class = PollListSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     def get_queryset(self):
#         polls = Poll.objects.annotate(
#             rating_user = models.Count('ratings', filter=models.Q(ratings__user=self.request.user)) #проверяем голосовал ли пользователь
#         ).annotate(
#             #middle_rate = models.Sum(models.F('ratings__rate')) / models.Count(models.F('ratings')) #средняя оценка # округляет до наименьшего целого
#             middle_rate=Round(models.Avg("ratings__rate"))
#         ).all()
#         return polls

# class PollDetailView(generics.RetrieveAPIView):
#     """Вывод Опроса"""
#     queryset = Poll.objects.filter()
#     serializer_class = PollDetailSerializer


# '''class AddRatingView(APIView):
#     """добавление рейтинга опросу"""
#     def post(self, request):
#         serializer = CreateRatingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=201)
#         else:
#             return Response(status=400)'''

# '''class PollListView(APIView):
#     """вывод списка опросов"""

#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     def get(self, request):
#         polls = Poll.objects.all()
#         serializer = PollListSerializer(polls, many=True)
#         return Response(serializer.data)'''

# '''class PollDetailView(APIView):
#     """Вывод Опроса"""

#     def get(self, request, pk):
#         poll = Poll.objects.get(id=pk)
#         serializer = PollDetailSerializer(poll)
#         return Response(serializer.data)'''

# '''class CreateNewPollView(APIView):
#     """Создание нового опроса"""

#     permission_classes = [permissions.IsAuthenticated]
#     def post(self, request):
#         poll = PollCreateSerializer(data=request.data)
#         if poll.is_valid():
#             poll.save() 
#             return Response(status=201)
#         else:
#             return Response(status=400)'''
