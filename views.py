from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, Enrollment, Question, Choice, Submission, Learner, Instructor

# Course List View
class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.order_by('-total_enrollment')[:10]

# Course Detail View
class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'

# Enroll view
def enroll(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        if request.user.is_authenticated:
            Enrollment.objects.get_or_create(user=request.user, course=course)
            course.total_enrollment += 1
            course.save()
        return redirect('onlinecourse:course_details', pk=course.id)
    return redirect('onlinecourse:course_details', pk=course_id)

# Helper function to extract answers from form
def extract_answers(request):
    submitted_answers = []
    for key, value in request.POST.items():
        if key.startswith('choice_'):
            try:
                choice_id = int(value)
                submitted_answers.append(choice_id)
            except (ValueError, TypeError):
                pass
    return submitted_answers

# Task 5: submit view function
def submit(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        user = request.user
        
        # Get or create enrollment
        enrollment, _ = Enrollment.objects.get_or_create(user=user, course=course)
        
        # Create a new submission
        submission = Submission.objects.create(enrollment=enrollment)
        
        # Extract submitted choice ids and attach to submission
        selected_choices = extract_answers(request)
        for choice_id in selected_choices:
            choice = Choice.objects.filter(pk=choice_id).first()
            if choice:
                submission.choices.add(choice)
        
        submission.save()
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)
    return HttpResponseBadRequest("Invalid request method.")

# Task 5: show_exam_result view function
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    selected_choice_ids = [choice.id for choice in submission.choices.all()]
    
    # Retrieve all questions associated with the course
    questions = Question.objects.filter(course=course)
    if not questions.exists():
        questions = Question.objects.filter(lesson__course=course)
    
    grade = 0
    total_marks = 0
    exam_results = []
    
    for question in questions:
        total_marks += question.grade
        is_correct = question.is_get_score(selected_choice_ids)
        if is_correct:
            grade += question.grade
        
        correct_answers = question.choice_set.filter(is_correct=True)
        exam_results.append({
            'question': question,
            'is_correct': is_correct,
            'correct_answers': correct_answers
        })
    
    percentage = round((grade / total_marks) * 100) if total_marks > 0 else 0
    passed = percentage >= 70
    
    context = {
        'course': course,
        'submission': submission,
        'grade': grade,
        'total_marks': total_marks,
        'percentage': percentage,
        'passed': passed,
        'exam_results': exam_results,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)

# Authentication views
def login_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')
    return render(request, 'onlinecourse/user_login_bootstrap.html')

def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')

def registration_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            login(request, user)
            return redirect('onlinecourse:index')
    return render(request, 'onlinecourse/user_registration_bootstrap.html')
