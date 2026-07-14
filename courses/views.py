from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Course


@login_required
def course_list_view(request):
    courses = Course.objects.all()

    query = request.GET.get('q', '').strip()
    difficulty = request.GET.get('difficulty', '')
    duration = request.GET.get('duration', '').strip()
    platform = request.GET.get('platform', '')

    if query:
        courses = courses.filter(course_name__icontains=query)

    if difficulty:
        courses = courses.filter(difficulty=difficulty)

    if platform:
        courses = courses.filter(platform=platform)

    if duration:
        courses = courses.filter(duration__icontains=duration)

    context = {
        'courses': courses[:100],  # cap for page performance
        'query': query,
        'selected_difficulty': difficulty,
        'selected_platform': platform,
        'duration': duration,
        'difficulty_choices': Course.DIFFICULTY_CHOICES,
        'platforms': Course.objects.values_list('platform', flat=True).distinct(),
    }
    return render(request, 'courses/course_list.html', context)
