from django.urls import path
from . import views

urlpatterns = [
    path('', views.recommend_form_view, name='recommend_form'),
    path('save/<int:course_id>/', views.save_course_view, name='save_course'),
    path('unsave/<int:course_id>/', views.unsave_course_view, name='unsave_course'),
    path('saved/', views.saved_courses_view, name='saved_courses'),
    path('history/', views.history_view, name='recommendation_history'),
]
