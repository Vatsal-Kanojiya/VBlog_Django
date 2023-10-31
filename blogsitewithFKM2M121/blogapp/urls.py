from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home,name='home'),
    path('home/', views.home,name='home'),
    
    path('newuser',views.newuser,name='newuser'),
    path('register',views.register,name='register'),
    path('userlogin',views.userlogin,name='userlogin'),
    path('logindone',views.logindone,name='logindone'),
    path('logoutdone',views.logoutdone,name='logoutdone'),
    path('userprofile/<str:u>/',views.userprofile,name='userprofile'),
    path('edituser/<str:u>/',views.edituser,name='edituser'),
    path('edituserdone/<str:u>/',views.edituserdone,name='edituserdone'),
    path('emailconfirmation/<str:u>/',views.emailconfirmation,name='emailconfirmation'),
    path('profilelist/<str:lt>/',views.profilelist,name='profilelist'),
    path('follow/<str:f>/',views.follow,name='follow'),
    path('unfollow/<str:u>/',views.unfollow,name='unfollow'),

    path('smartblogupgrade/<str:u>/',views.smartblogupgrade,name='smartblogupgrade'),
    path('smartblogsuccess/',views.smartblogsuccess,name='smartblogsuccess'),

    path('genre/<str:g>/', views.genre,name='genre'),
    path('latest', views.latest,name='latest'),
    path('popular', views.popular,name='popular'),
    #path('time/<str:dt>/', views.time,name='time'),
    #path('authorfilter/<str:a>/', views.authorfilter,name='authorfilter'),
    path('tag', views.tag,name='tag'),
    
    path('blog/<str:b>/', views.blogview,name='blog'),
    
    path('comment/<str:b>/', views.commentview,name='comment'),
    path('like/<str:b>/', views.like,name='like'),

    path('newblog/', views.newblog,name='newblog'),
    path('createblog/', views.createblog,name='createblog'),



] + static(settings.MEDIA_URL,document_root=(settings.MEDIA_ROOT))