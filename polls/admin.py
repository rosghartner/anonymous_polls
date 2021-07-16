from django.contrib import admin
from .models import Question, Answer, Choice, Choices, Poll, Rating

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class PollAdmin(admin.ModelAdmin):
    list_display = ('title','id')
    inlines = [QuestionInline]
    list_filter = ('title',)
    

class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'question',
 #       'lock_other',
    )
    inlines = [AnswerInline]
    

class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'answer',
        'question',
    )
    list_filter = ('question',)


class ChoiceAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'answer',
    )
    #list_filter = ('user', 'poll',)

class ChoicesAdmin(admin.ModelAdmin): #закоментированно для анонимности
    list_display = (
        'user',
        'poll',
        'created',
    )

class RatingAdmin(admin.ModelAdmin):
    list_display = ('rate', 'user', 'poll',)


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Choices, ChoicesAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Rating, RatingAdmin)