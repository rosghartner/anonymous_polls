from rest_framework import permissions, generics, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models
 
from .models import Poll, Question
from .serializers import PollListSerializer, PollDetailSerializer, PollCreateSerializer, CreateRatingSerializer


class PollListView(generics.ListAPIView):
    """вывод списка опросов"""
    serializer_class = PollListSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        
        print(self.request.user)
        polls = Poll.objects.all().annotate(
            rating_user = models.Count('ratings', filter=models.Q(ratings__user=self.request.user)) #проверяем голосовал ли пользователь
        ).annotate(
            middle_rate = models.Sum(models.F('ratings__rate')) / models.Count(models.F('ratings')) #средняя оценка
        )
        return polls


class PollDetailView(generics.RetrieveAPIView):
    """Вывод Опроса"""
    queryset = Poll.objects.filter()
    serializer_class = PollDetailSerializer


class CreateNewPollView(generics.CreateAPIView):
    """Создание нового опроса"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PollCreateSerializer


class UpdatePollView(generics.UpdateAPIView):
    """Редактирование Опроса"""
    serializer_class = PollCreateSerializer
    queryset = Poll.objects.all()


class AddRatingView(generics.CreateAPIView):
    """добавление рейтинга опросу"""

    serializer_class = CreateRatingSerializer



'''class AddRatingView(APIView):
    """добавление рейтинга опросу"""
    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)'''

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
