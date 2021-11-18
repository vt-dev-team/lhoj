from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.SubmissionList, name='submissionList'),
    path('submit/', views.newSubmission, name='newSubmission'),
    path('latest/', views.FindSubmission, name='latestSubmission'),
    path('<int:submission_id>/', views.SubmissionDetail, name='submissionDetail'),
    path('<int:submission_id>/edit/', views.SubmissionEdit, name='submissionEdit'),
    path('<int:submission_id>/edit/case/', views.UpdateOneCase, name='updateOneCase'),
]