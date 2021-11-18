from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.PostList, name='PostList'),
    path('sections/', views.SectionList, name='SectionList'),
    path('post/<int:post_id>/', views.PostShow, name='PostShow'),
    path('post/<int:post_id>/edit/', views.editPost, name='PostEdit'),
    path('post/<int:post_id>/delete/', views.DeletePost, name='DeletePost'),
    path('post/new/', views.newPost, name='newPost'),
    path('comment/new/', views.newComment, name='newComment'),
    path('comment/<int:comment_id>/delete/', views.DeleteComment, name='deleteComment'),
]
