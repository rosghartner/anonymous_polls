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


class PollCreateSerializer(serializers.ModelSerializer):
    """Создание опроса"""
    questions = QuestionSerializer(many=True)
    id = serializers.IntegerField(required=False)
    
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


    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.save() #обновляем тайтл и дескрипшен

    #     questions_data = validated_data.pop('questions') #извлекаем вопросы
    #     print('квестион дата ------------',questions_data)
    #     questions_data_dict = dict((i.id, i)for i in instance.questions.all())#создаем словарь с айдишниками
    #     print('словарь--------------',questions_data_dict)
    #     for question_data in questions_data:
    #         print('data_item ---------------', question_data)
    #         answers_data = question_data.pop('answers') #извлекаем все ответы для каждого вопроса
    #         print('answers_data---------------', answers_data)
    #         print('instance --------------', instance)
    #         print('validated_data-------------', validated_data)
    #         question_data.question=question_data.get('question', question_data.question)
    #         question_data.save()
    #         for answer_data in answers_data:
    #             pass        
    #     return instance





    # def update(self, instance, validated_data): 
    #     print('==============INSTANCE=============' ,instance)
        
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.save()

    #     questions_data = validated_data.get('questions')
    #     print('*'*15, 'question data:', *questions_data, '*'*15, sep='\n')
    #     for question in questions_data:
    #         question_id = question.get('id', None)
    #         print('*'*15, 'question id:', question, '*'*15)
    #         answers = question.get('answers')
    #         if question_id:
    #             quest_item = Question.objects.get(id=question_id, poll=instance)
    #             quest_item.question = question.get('question', quest_item.question)
    #             for answer in answers:
    #                 answer_id = answer.get('id', None)
    #                 print('*'*15, 'question id:', question_id, '*'*15)
    #                 if answer_id:
    #                     answer_item = Answer.objects.get(id=answer_id, question=instance)
    #                     answer_item.answer = answer.get('answer', answer_item.answer)
    #                     answer_item.save()
    #                 else:
    #                     print('create answer was here')
    #             quest_item.save()
    #         else:
    #             print('create question was here')#Question.objects.create()
    #         print(question)
    #         for answer in answers:
    #             print(answer)
    #     return instance


        '''def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        poll = Poll.objects.create(**validated_data)
        for question_data in questions_data:
            answers_data = question_data.pop('answers')
            question = Question.objects.create(poll = poll, **question_data)
            for answer_data in answers_data: 
                Answer.objects.create(question=question, **answer_data)
        return poll'''

