from rest_framework import serializers

from .models import Poll, Question, Answer


class PollListSerializer(serializers.ModelSerializer):
    """Список опросов"""
    class Meta:
        model = Poll
        fields = ('id', 'title')


class AnswerSerializer(serializers.ModelSerializer):
    """Ответы"""
    class Meta:
        model = Answer
        fields = ('answer',)


class QuestionSerializer(serializers.ModelSerializer):
    """Вопросы"""    
    answers = AnswerSerializer(many=True)
    
    class Meta:
        model = Question
        fields = ('question','answers')

class PollDetailSerializer(serializers.ModelSerializer):
    """Опрос"""
    questions = QuestionSerializer(many=True)
    creator = serializers.SlugRelatedField(slug_field='username', read_only=True)
    
    class Meta:
        model = Poll
        fields = "__all__"

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        poll = Poll.objects.create(**validated_data)
        for question_data in questions_data:
            answers_data = question_data.pop('answers')
            question = Question.objects.create(poll = poll, **question_data)
            for answer_data in answers_data: 
                Answer.objects.create(question=question, **answer_data)
        return poll

