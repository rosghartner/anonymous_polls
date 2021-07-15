from rest_framework import serializers


from .models import Choice, Poll, Question, Answer, Rating


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
        fields = ('answer', 'id')

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


# class PollDetailSerializer(serializers.ModelSerializer):
#     """Опрос"""
#     questions = QuestionSerializer(many=True)
#     #creator = serializers.SlugRelatedField(slug_field='username', read_only=True) #выводит юзернейм вместо айдишника
    
#     class Meta:
#         model = Poll
#         fields = ('title', 'id', 'creator', 'description', 'questions')


class PollCreateSerializer(serializers.ModelSerializer):
    """Создание опроса"""
    questions = QuestionSerializer(many=True)
    # id = serializers.IntegerField(required=False)
    
    class Meta:
        model = Poll
        fields = ('title', 'id', 'creator', 'description', 'questions',)

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

    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.description = validated_data.get('description', instance.description)
    #     print('-----------------',instance.questions.all())
    #     questions_data = validated_data.pop('questions')
    #     questions = instance.questions.all()
    #     print(questions, '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    #     # questions_data_dict = dict((i.id, i)for i in instance.questions.all())
    #     # print('словарь--------------',questions_data_dict)
    #     for question_data in questions_data:
    #         #question = Question.objects.get(poll = instance)    #надо разобраться как получить один экземпляр
    #         #print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@', question)
    #         print('----------------question_data ------------',question_data)
    #         print('----------------Question.question ------------',Question.question)
    #         answers_data = question_data.pop('answers')
    #         for answer_data in answers_data:
    #             print('----------------answer_data ------------',answer_data)

    #     instance.save() #обновляем тайтл и дескрипшен
    #     return instance

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

# class AnswerChoiceSerializer(serializers.ModelSerializer):
#     """question id for choices"""
#     id = Answer.id
#     class Meta:
#         model = Answer
#         fields = ('id',)

# class QuestionChoiceSerializer(serializers.ModelSerializer):
#     """question id for choices"""
#     answer = AnswerChoiceSerializer(many=True)
#     id = serializers.IntegerField()
#     class Meta:
#         model = Question
#         fields = ('id', 'answer')


class CreateChoiceSerializer(serializers.ModelSerializer):
    """Прохождение опроса"""
    # questions = QuestionChoiceSerializer(many=True)

    class Meta:
        model = Choice
        fields = ('user', 'poll', 'question', 'answer')
        
    # def create(self, validated_data):
    #     print(validated_data)
    #     questions_data = validated_data.pop('questions')
    #     for question_data in questions_data:
    #         answers_data = question_data.pop('answer')
    #         question = question_data.get('id')
    #         print('****************************o hi mark', question)
    #         for answer_data in answers_data:
    #             choice, _ = Choice.objects.create(
    #                 user = validated_data.get('user', None),
    #                 poll = validated_data.get('poll', None),
    #                 question = question,
    #                 answer = answer_data.pop('id', None),
                    
    #                 )
    #     return True