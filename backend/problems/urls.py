from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.ProblemsList, name='problemList'),
    path('new/', views.ProblemNew, name='problemNew'),
    path('latest/', views.ProblemLatest, name='problemLatest'),
    path('<int:problem_id>/', views.ProblemDetail, name='problemDetail'),
    path('<int:problem_id>/data/', views.GetData, name='GetData'),
    path('<int:problem_id>/upload/', views.UploadData, name='dataUpload'),
    path('<int:problem_id>/edit/', views.ProblemEdit, name='problemEdit'),
    path('<int:problem_id>/download/', views.DataDownload, name='downloadData'),
    path('<int:problem_id>/attachments/', views.AttachementsDownload, name='downloadAttachements'),
]