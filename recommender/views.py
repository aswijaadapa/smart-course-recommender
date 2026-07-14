from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from courses.models import Course
from .forms import RecommendationForm
from .models import SavedCourse, RecommendationHistory
from . import ml_engine


@login_required
def recommend_form_view(request):
    profile = request.user.userprofile

    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            try:
                results = ml_engine.get_recommendations(
                    skills=data['skills'],
                    interests=data['interests'],
                    career_goal=data['career_goal'],
                    experience_level=data['experience_level'],
                    top_n=10,
                )
            except FileNotFoundError:
                messages.error(
                    request,
                    "The recommendation model hasn't been trained yet. "
                    "Run 'python manage.py train_model' first."
                )
                return redirect('recommend_form')

            # Save this search to the user's recommendation history
            history = RecommendationHistory.objects.create(
                user=request.user,
                query_text=ml_engine.build_profile_text(
                    data['skills'], data['interests'], data['career_goal'], data['experience_level']
                ),
                career_goal=data['career_goal'],
            )
            history.recommended_courses.set([course for course, _ in results])

            saved_ids = set(
                SavedCourse.objects.filter(user=request.user).values_list('course_id', flat=True)
            )

            context = {
                'results': results,
                'saved_ids': saved_ids,
                'form_data': data,
            }
            return render(request, 'recommender/results.html', context)
    else:
        # Pre-fill the form from the user's saved profile, if available
        initial = {
            'skills': profile.current_skills,
            'interests': profile.interests,
            'career_goal': profile.career_goal,
            'experience_level': profile.experience_level or 'Beginner',
            'weekly_study_hours': profile.weekly_study_hours,
            'preferred_platform': profile.preferred_platform,
        }
        form = RecommendationForm(initial=initial)

    return render(request, 'recommender/recommend_form.html', {'form': form})


@login_required
def save_course_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    saved, created = SavedCourse.objects.get_or_create(user=request.user, course=course)
    if created:
        messages.success(request, f'"{course.course_name}" saved to your favorites.')
    else:
        messages.info(request, f'"{course.course_name}" is already in your favorites.')
    return redirect(request.META.get('HTTP_REFERER', 'recommend_form'))


@login_required
def unsave_course_view(request, course_id):
    SavedCourse.objects.filter(user=request.user, course_id=course_id).delete()
    messages.success(request, "Removed from your favorites.")
    return redirect('saved_courses')


@login_required
def saved_courses_view(request):
    saved = SavedCourse.objects.filter(user=request.user).select_related('course')
    return render(request, 'recommender/saved_courses.html', {'saved': saved})


@login_required
def history_view(request):
    history = RecommendationHistory.objects.filter(user=request.user).prefetch_related('recommended_courses')
    return render(request, 'recommender/history.html', {'history': history})
