from django.urls import path
from . import views

urlpatterns = [
    path('user-invalid', views.user_invalid, name='user_invalid'),
    path('refund-done', views.refund_done, name='refund_done'),
    path('task-perform', views.task_perform, name='task_perform'),
    path('create-task', views.create_task, name='create_task'),
    path('user-no-perms', views.user_no_perms, name='user_no_perms'),
    path('admin-page', views.admin_page, name='admin_page'),
    path('getwork', views.get_work, name='get_work'),
    path('<str:error>', views.home_space, name='home'),
    path('', views.home_space, name='home'),

]