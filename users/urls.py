from django.urls import path
from users import views

app_name = 'users'
urlpatterns = [
    path('login/',view=views.login_request,name='login'),
    path('logout/',view=views.logout_request,name='logout'),
    path('register/',view=views.register_request,name='register'),
]