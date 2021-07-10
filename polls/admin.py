from django.contrib import admin
from .models import Question, Answer, Choice, Poll, Rating

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
        'user',
        'poll',
        'question',
        'answer',
        'created',
    )
    list_filter = ('user', 'poll',)

class RatingAdmin(admin.ModelAdmin):
    list_display = ('rate', 'user', 'poll',)


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Rating, RatingAdmin)