from django.urls import path

from . import views

urlpatterns = [
    path('_login/', views.LoginUser, name='loginedUser'),
    path('logout/', views.Logout, name='logoutUser'),
    path('login/', views.Login, name='userLogin'),
    path('reg/', views.Register, name='userRegister'),
    path('rank/', views.RankList, name='ranklist'),
    path('contacts/', views.ContactList, name='contactlist'),
    path('message/', views.MessageList, name='messagelist'),
    path('send_message/', views.NewMessage, name='newMessage'),
    path('find/', views.UserSimpleList, name='userFind'),
    path('<str:user_id>/', views.UserInfo, name='userInfo'),
    path('<str:user_id>/modify/', views.UserModify, name='userModify'),
]
