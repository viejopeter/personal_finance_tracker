from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Account
from django.views.decorators.http import require_POST

def accounts_ls(request):
    context = {}
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        print(accounts)
        context['accounts'] = accounts
        return render(request,"accounts/accounts_ls.html",context=context)
    return None

def create_account(request):
    if request.method == 'POST':
        account_name = request.POST.get('name')
        initial_amount = request.POST.get('initial_amount')
        if request.FILES.get('icon'):
            icon = request.FILES.get('icon')
        Account.objects.create(user=request.user, name=account_name, initial_amount=initial_amount, icon=icon)
        messages.success(request, 'Account Created Successfully')
        return redirect("accounts:accounts_ls")

    return render(request,"accounts/account_form.html",context = {'action': 'Create'})

def update_account(request,id_account):
    account = get_object_or_404(Account, pk=id_account)
    if request.method == 'POST':
        account.name = request.POST.get('name')
        account.initial_amount = request.POST.get('initial_amount')
        if request.FILES.get('icon'):
            account.icon = request.FILES.get('icon')
        account.save()
        messages.success(request, 'Account Updated Successfully')
        return redirect("accounts:accounts_ls")

    return render(request,"accounts/account_form.html",context = {'action': 'Update', 'account': account})

@require_POST
def delete_account(request, id_account):
    try:
        account = get_object_or_404(Account, pk=id_account)
        account.delete()
        messages.success(request, 'Account Deleted Successfully')
    except Exception as e:
        messages.error(request, f'Error deleting account: {str(e)}')
    return redirect("accounts:accounts_ls")

