from django.db import models
from django.conf import settings


class Poll(models.Model):
    """Опрос"""
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts_created')
    title = models.CharField('Название', max_length=240)
    description = models.TextField("Описание")

    def __str__(self):
           return self.title

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Question(models.Model):
    """Вопрос"""
    poll = models.ForeignKey(Poll, verbose_name="Poll", on_delete=models.CASCADE, related_name="questions")
    question = models.CharField('вопрос', max_length=4096)
    # lock_other = models.BooleanField(default=False)
    

    def __str__(self):
           return self.question

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    """Ответ"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer = models.CharField('ответ', max_length=4096)

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Choice(models.Model):
    """Вариант ответа"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    answer = models.ForeignKey(Answer, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer.title

