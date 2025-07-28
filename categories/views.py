from django.contrib.messages.context_processors import messages
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib import messages
from categories.models import Category
from users.models import UserExtend


class CategoryListView(View):

    def get(self,request):
        context = {}
        user = get_object_or_404(UserExtend,user_id=request.user.id)
        categories = user.categories.all()
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

        user_extend = get_object_or_404(UserExtend,user_id=request.user.id)

        category = request.POST['category']
        category_type = request.POST['category_type']
        user = request.user
        #Create the category in the model
        new_category = Category.objects.create(category=category,category_type=category_type,user=user)
        #Create the category in relationship
        user_extend.categories.add(new_category)
        context = {
            'action': 'Create',
            'categories': user_extend.categories.all()
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
     pass


class CategoryDeleteView(View):

    pass