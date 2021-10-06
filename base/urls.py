from django.urls import path
from .views import ( home,room,createRoom,updateRoom,deleteRoom,appLogin,appLogout,appRegisterUser,deleteMessage,userProfile )

urlpatterns = [
    path('login/',appLogin,name='login'),
    path('register/',appRegisterUser,name='register'),
    path('logout/',appLogout,name='logout'),
    path('',home,name="home"),
    path('room/<str:slug>/',room,name="room"),
    path('create-room/',createRoom,name="create-room"),
    path('update-room/<str:slug>/',updateRoom,name="update-room"),
    path('delete-room/<str:slug>/',deleteRoom,name="delete-room"),
    path('delete-message/<str:slug>/',deleteMessage,name="delete-message"),
    path('profile/<str:user_id>/',userProfile,name="user-profile")
]