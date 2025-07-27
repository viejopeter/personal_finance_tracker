from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns =[
    path('',view=views.accounts_ls,name='accounts_ls'),
    path('create/',view=views.create_account,name='create_account'),
    path('<int:id_account>/edit/',view=views.update_account,name='update_account'),
    path('<int:id_account>/delete/',view=views.delete_account,name='delete_account'),
]