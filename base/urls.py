from django.urls import path
from .views import Tasklist, Taskdetail, Taskcreate, Taskupdate, Taskdelete, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('', Tasklist.as_view(), name='tasklist'),
    path('taskdetail/<int:pk>/', Taskdetail.as_view(), name='taskdetail'),
    path('taskcreate/', Taskcreate.as_view(), name='taskcreate'),
    path('taskedit/<int:pk>/', Taskupdate.as_view(), name='taskedit'),
    path('taskdelete/<int:pk>/', Taskdelete.as_view(), name='taskdelete'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='base/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='base/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='base/password_reset_form.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='base/password_reset_done.html'), name='password_reset_complete'),

]