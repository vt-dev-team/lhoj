from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.ContestList, name='contestList'),
    path('new/', views.ContestNew, name='contestNew'),
    path('latest/', views.ContestLatest, name='contestLatest'),
    path('<int:contest_id>/', views.ContestDetail, name='contestShow'),
    path('<int:contest_id>/edit/', views.ContestEdit, name='contestEdit'),
    path('<int:contest_id>/delete/', views.ContestDelete, name='contestDelete'),
    path('<int:contest_id>/rank/', views.ContestRank, name='contestRank'),
]