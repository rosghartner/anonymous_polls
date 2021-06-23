from rest_framework import permissions, generics
#from rest_framework.response import Response
#from rest_framework.views import APIView

from .models import Poll
from .serializers import PollListSerializer, PollDetailSerializer, PollCreateSerializer


class PollListView(generics.ListAPIView):
    """вывод списка опросов"""
    serializer_class = PollListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        polls = Poll.objects.all()
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
    #queryset = Poll.objects.all()


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
