from django.contrib import admin
# Task 2: Seven imported classes from .models
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission

# ChoiceInline implementation
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

# QuestionInline implementation
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2

# QuestionAdmin implementation with ChoiceInline
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_text', 'grade', 'course')
    search_fields = ['question_text']

# LessonAdmin implementation with QuestionInline
class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'course', 'order']
    list_filter = ['course']

# CourseAdmin implementation
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 2

class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ('name', 'pub_date', 'total_enrollment')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']

# Register models in admin site
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)

admin.site.site_header = 'OnlineCourse Administration'
admin.site.site_title = 'OnlineCourse Admin Portal'
