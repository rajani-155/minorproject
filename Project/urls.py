
from django.contrib import admin
from django.urls import path
from app.views import Home,ViewAttend,AddStudent,TakeAttendence,Login,Logout,Edit

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Home,name='home'),
    path('login',Login,name='login'),
    path('logout',Logout,name='logout'),
    path('viewattend',ViewAttend,name='viewattendenct'),
    path('addstd',AddStudent,name='addstudent'),
    path('attendence',TakeAttendence,name='takeattendence'),
    path('edit',Edit,name='edit')
]
