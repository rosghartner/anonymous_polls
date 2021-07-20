from rest_framework import serializers

from .models import Choice, Choices, Poll, Question, Answer, Rating


class PollListSerializer(serializers.ModelSerializer):
    """Список опросов"""
    rating_user = serializers.BooleanField()
    middle_rate = serializers.FloatField()
    class Meta:
        model = Poll
        fields = ('id', 'title', 'rating_user', 'middle_rate') #


class AnswerSerializer(serializers.ModelSerializer):
    """Ответы"""
    class Meta:
        model = Answer
        fields = ('answer', 'id',)



class AnswerCreateSerializer(serializers.ModelSerializer):
    """Ответы"""
    class Meta:
        model = Answer
        fields = ('answer', 'id', 'question')


class QuestionSerializer(serializers.ModelSerializer):
    """Вопросы"""    
    answers = AnswerSerializer(many=True)
    
    class Meta:
        model = Question
        fields = ('question', 'id', 'answers') 




class QuestionCreateSerializer(serializers.ModelSerializer):
    """Вопросы"""    
    answers = AnswerSerializer(many=True)
    
    class Meta:
        model = Question
        fields = ('poll', 'question', 'id', 'answers') 

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        question = Question.objects.create(**validated_data)
        for answer_data in answers_data: 
            Answer.objects.create(question=question, **answer_data)
        return question

class QuestionUpdateSerializer(serializers.ModelSerializer):
    """Вопросы"""    
    
    class Meta:
        model = Question
        fields = ('question', 'id') 




class PollCreateSerializer(serializers.ModelSerializer):
    """Создание опроса"""
    questions = QuestionSerializer(many=True)
    # id = serializers.IntegerField(required=False)
    
    class Meta:
        model = Poll
        fields = ('title', 'id', 'creator', 'description', 'questions', )

    def create(self, validated_data): #validated_data - данные которые мы получаем с клиентской стороны
        questions_data = validated_data.pop('questions')
        poll = Poll.objects.create(**validated_data)
        for question_data in questions_data:
            answers_data = question_data.pop('answers')
            question = Question.objects.create(poll = poll, **question_data)
            for answer_data in answers_data: 
                Answer.objects.create(question=question, **answer_data)
        return poll

class PollUpdateSerializer(serializers.ModelSerializer):
    """Создание опроса"""

    class Meta:
        model = Poll
        fields = ('title', 'id', 'creator', 'description')


class CreateRatingSerializer(serializers.ModelSerializer):
    """Голосование за опрос"""
    #middle_rate = serializers.FloatField()
    class Meta:
        model = Rating
        fields = ('rate','poll', 'user')

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create( #возвращает кортеж, по этому используем переменную _ 
            user = validated_data.get('user', None),
            poll = validated_data.get('poll', None),
            defaults={'rate': validated_data.get('rate')}
        )
        return rating


class ChoiceSerializer(serializers.ModelSerializer):
    """Ы"""
    # total_a = serializers.SerializerMethodField()
    # def get_total_a(self, obj):
    #     return obj.choice.count()
    class Meta:
        model = Choice
        fields = ('question', 'answer',)

    


class CreateChoiceSerializer(serializers.ModelSerializer):
    """Прохождение опроса"""
    choice = ChoiceSerializer(many=True, read_only=True)
    class Meta:
        model = Choices
        fields = ('user', 'poll', 'choice')

    def create(self, validated_data):
        choices_data = validated_data.pop('choice')
        choices, _ = Choices.objects.update_or_create(
            # user = validated_data.get('user', None),
            # poll = validated_data.get('poll', None)
            **validated_data
        )
        for choice_data in choices_data:
            Choice.objects.update_or_create(
                choices = choices,
                question = choice_data.get('question', None),
                defaults={'answer': choice_data.get('answer')}
            )
        return choices

class AnswerSerializer1(serializers.ModelSerializer):
    """Ответы"""
    #choice = ChoiceSerializer(many=True, read_only=True)
    total_answer = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ('answer', 'id',  'total_answer',)#'choice',

    def get_total_answer(self,obj):
        return Choice.objects.filter(answer=obj).count()

class QuestionSerializer1(serializers.ModelSerializer):
    """Вопросы"""    
    answers = AnswerSerializer1(many=True)
    class Meta:
        model = Question
        fields = ('question', 'id', 'answers') 

class PollDetailSerializer(serializers.ModelSerializer):
    """Опрос"""
    questions = QuestionSerializer1(many=True)
    total_complete = serializers.IntegerField()
    
    class Meta:
        model = Poll
        fields = ('title', 'id', 'creator', 'description', 'total_complete', 'questions',)