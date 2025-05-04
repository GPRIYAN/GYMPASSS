from django.urls import path
from GymApp import views

urlpatterns = [
    path('',views.Home,name="Home"),
    path('signup',views.signup,name="signup"),
    path('login',views.handlelogin,name="handlelogin"),
    path('logout',views.handleLogout,name="handleLogout"),
    path('contact',views.contact,name="contact"),
    path('join',views.enroll,name="enroll"),
    path('profile',views.profile,name="profile"),
    path('attendance',views.attendance,name="attendance"),
    path('allworkout',views.allworkout,name="allworkout"),
    path('bicepsplan/<str:level>/',views.bicepsplan,name="bicepsplan"),
    path('chat/<str:room_name>/', views.chatRoom, name='chatroom'),
    path('createroom', views.createRoom, name='createroom'),
    path("query-groq", views.chat_with_groq, name="groq_ai_query"),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('meeting/',views.videocall, name='meeting'),
    path('join/',views.join_room, name='join_room'),
    path('logout/',views.logout_view, name='logout'),
]
