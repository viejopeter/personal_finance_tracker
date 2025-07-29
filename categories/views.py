from django.contrib.messages.context_processors import messages
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from categories.models import Category

class CategoryListView(View):

    def get(self,request):
        context = {}
        categories = Category.objects.filter(user=request.user)
        context['categories'] = categories
        return render(request,'categories/categories_ls.html',context=context)

class CategoryCreateView(View):

    def get(self,request):

        context = {
            'action': 'Create',
            'category_type': Category.category_type_options
        }

        return render(request,"categories/category_form.html",context=context)

    def post(self,request):

        category = request.POST['category']
        category_type = request.POST['category_type']

        #Create the category in the model
        Category.objects.create(category=category,category_type=category_type,user=request.user)
        categories = Category.objects.filter(user=request.user)

        context = {
            'action': 'Create',
            'categories': categories
        }
        messages.success(request, 'Category Added Successfully')
        return render(request,'categories/categories_ls.html',context=context)

class CategoryEditView(View):

    def get(self,request,id_category):
       category = get_object_or_404(Category,id=id_category)
       category_type = Category.category_type_options
       context = {
            'action': 'Edit',
            'category_type': category_type,
            'category': category
       }

       return render(request,"categories/category_form.html",context=context)

    def post(self,request, *args, **kwargs):

       #Bring the variables from POST request
       category_name = request.POST['category']
       category_type = request.POST['category_type']

       #Using kwargs bring the id in url
       id_category = kwargs['id_category']

       category = get_object_or_404(Category,id=id_category)
       category.category = category_name
       category.category_type = category_type
       category.user = request.user
       category.save()

       categories = Category.objects.filter(user=request.user)

       context = {
            'action': 'Edit',
            'categories': categories
       }
       messages.success(request, 'Category Updated Successfully')
       return render(request,'categories/categories_ls.html',context=context)

class CategoryDeleteView(View):

    def post(self,request, *args, **kwargs):
        id_category = kwargs.get('id_category')
        try:
            category = get_object_or_404(Category,pk=id_category)
            category.delete()
            messages.success(request, 'Category Deleted Successfully')
        except Http404:
            messages.error(request, 'Category Not Found')

        return redirect('categories:category_ls')
