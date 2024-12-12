
from django.urls import path
from .views import (admin_home_view, create_user_view, update_user_view, delete_user_view,
    signup_view, login_view, home_view, logout_view)


urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
    path('admin-home/', admin_home_view, name='admin_home'), 
    path('admin-home/create/', create_user_view, name='create_user'),  
    path('admin-home/update/<int:user_id>/', update_user_view, name='update_user'),  
    path('admin-home/delete/<int:user_id>/', delete_user_view, name='delete_user'), 
]
