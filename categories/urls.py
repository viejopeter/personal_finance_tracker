from django.urls import path

from categories.views import CategoryListView,CategoryCreateView,CategoryEditView,CategoryDeleteView

app_name = "categories"

urlpatterns = [
    path('',CategoryListView.as_view(),name='category_ls'),
    path('create/',CategoryCreateView.as_view(),name='category_create'),
    path('<int:id_category>/edit/',CategoryEditView.as_view(),name='category_edit'),
    path('<int:id_category>/delete/',CategoryDeleteView.as_view(),name='category_delete'),
]