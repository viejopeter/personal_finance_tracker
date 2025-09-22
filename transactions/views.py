from django.contrib.messages.context_processors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q
from categories.models import Category
from transactions.models import Transaction
from accounts.models import Account
from datetime import datetime
from django.contrib import messages
from decimal import Decimal

def update_account_balances(type, amount, origin_account, destination_account=None, reverse=False):
    amount_value = Decimal(str(amount))
    if reverse:
        amount_value = -amount_value
    if type == 'income':
        if origin_account:
            origin_account.balance += amount_value
            origin_account.save()
    elif type == 'expense':
        if origin_account:
            origin_account.balance -= amount_value
            origin_account.save()
    elif type == 'transfer':
        if origin_account and destination_account:
            origin_account.balance -= amount_value
            origin_account.save()
            destination_account.balance += amount_value
            destination_account.save()

class TransactionsListView(View):
    def get(self, request):
        context = {}
        transactions = Transaction.objects.filter(
            Q(origin_account__user=request.user) | Q(destination_account__user=request.user)
        )
        context['transactions'] = transactions
        return render(request,'transactions/transactions_ls.html',context=context)

class TransactionsCreateView(View):
    def get(self, request):
        transaction_type = Transaction.choices
        categories_ls = Category.objects.filter(user=request.user)
        categories_by_type = {}
        for t_value, t_label in transaction_type:
            # Filter categories by type for the current user and build a dictionary for JS
            filtered = categories_ls.filter(category_type=t_value)
            categories_by_type[t_value] = [(c.id, c.category) for c in filtered]
        # Get all accounts for the current user for account selection
        accounts_ls = Account.objects.filter(user=request.user).values('id','name')
        accounts_select = [(a['id'],a['name']) for a in accounts_ls]
        context={
            'action': 'Create',
            'transaction_type': transaction_type,
            'accounts': accounts_select,
            'categories_by_type': categories_by_type,
        }
        return render(request,"transactions/transactions_form.html",context=context)

    def post(self, request):
        type = request.POST.get('type')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        account_id = request.POST.get('account')
        to_account_id = request.POST.get('to_account')
        date_str = request.POST.get('date')
        errors = []
        # Validate required fields
        if not type:
            errors.append('Type is required.')
        if not description:
            errors.append('Description is required.')
        if not amount:
            errors.append('Amount is required.')
        if not account_id:
            errors.append('Account is required.')
        if not date_str:
            errors.append('Date is required.')
        # Category validation
        category_id = request.POST.get('category') if type in ['income', 'expense'] else None
        if type in ['income', 'expense'] and not category_id:
            errors.append('Category is required for income or expense.')
        # Destination account validation
        if type == 'transfer':
            if not to_account_id:
                errors.append('Destination account is required for transfer.')
        # If errors, send as Django error messages and re-render form
        if errors:
            for error in errors:
                messages.error(request, error, extra_tags='danger')
            transaction_type = Transaction.choices
            categories_ls = Category.objects.filter(user=request.user)
            categories_by_type = {}
            for t_value, t_label in transaction_type:
                filtered = categories_ls.filter(category_type=t_value)
                categories_by_type[t_value] = [(c.id, c.category) for c in filtered]
            accounts_ls = Account.objects.filter(user=request.user).values('id','name')
            accounts_select = [(a['id'],a['name']) for a in accounts_ls]
            context = {
                'action': 'Create',
                'transaction_type': transaction_type,
                'accounts': accounts_select,
                'categories_by_type': categories_by_type,
            }
            return render(request, "transactions/transactions_form.html", context)

        # Get model instances
        category = Category.objects.get(id=category_id) if category_id else None
        origin_account = Account.objects.get(id=account_id) if account_id else None
        destination_account = Account.objects.get(id=to_account_id) if (type == 'transfer' and to_account_id) else None
        date_value = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        Transaction.objects.create(
            type=type,
            description=description,
            amount=amount,
            origin_account=origin_account,
            destination_account=destination_account,
            datetime=date_value,
            category=category,
        )
        update_account_balances(type, amount, origin_account, destination_account)
        messages.success(request, 'Transaction created Successfully!')
        return redirect('transactions:transactions_ls')


class TransactionsUpdateView(View):
    def get(self, request, *args, **kwargs):
        id_transaction = kwargs.get('id_transaction')
        transaction = get_object_or_404(Transaction, id=id_transaction)
        date_str = transaction.datetime.strftime('%Y-%m-%dT%H:%M') if transaction.datetime else ''
        transaction_type = Transaction.choices
        categories_ls = Category.objects.filter(user=request.user)
        categories_by_type = {}
        for t_value, t_label in transaction_type:
            # Filter categories by type for the current user and build a dictionary for JS
            filtered = categories_ls.filter(category_type=t_value)
            categories_by_type[t_value] = [(c.id, c.category) for c in filtered]
        # Get all accounts for the current user for account selection
        accounts_ls = Account.objects.filter(user=request.user).values('id','name')
        accounts_select = [(a['id'],a['name']) for a in accounts_ls]
        # Format transaction date for the input field
        date_str = transaction.datetime.strftime('%Y-%m-%dT%H:%M') if transaction.datetime else ''
        # Prepare context for rendering the update form
        context = {
            'id_transaction': id_transaction,  # Transaction ID for reference
            'action': 'Update',                # Action label for the form
            'transaction': transaction,        # Transaction instance to edit
            'date': date_str,                  # Formatted date for input
            'transaction_type': transaction_type, # List of transaction types
            'accounts': accounts_select,       # List of user's accounts
            'categories_by_type': categories_by_type, # Filtered categories by type
        }
        return render(request, "transactions/transactions_form.html", context)

    def post(self, request, *args, **kwargs):
        id_transaction = kwargs.get('id_transaction')
        transaction = get_object_or_404(Transaction, id=id_transaction)
        # Store old values for reversal
        old_type = transaction.type
        old_amount = transaction.amount
        old_origin = transaction.origin_account
        old_dest = transaction.destination_account
        update_account_balances(old_type, old_amount, old_origin, old_dest, reverse=True)
        # Get new values from the request
        type = request.POST.get('type')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        account_id = request.POST.get('account')
        to_account_id = request.POST.get('to_account')
        date_str = request.POST.get('date')
        errors = []
        # Validate required fields
        if not type:
            errors.append('Type is required.')
        if not description:
            errors.append('Description is required.')
        if not amount:
            errors.append('Amount is required.')
        if not account_id:
            errors.append('Account is required.')
        if not date_str:
            errors.append('Date is required.')
        # Category validation
        category_id = request.POST.get('category') if type in ['income', 'expense'] else None
        if type in ['income', 'expense'] and not category_id:
            errors.append('Category is required for income or expense.')
        # Destination account validation
        if type == 'transfer':
            if not to_account_id:
                errors.append('Destination account is required for transfer.')
        # If errors, send as Django error messages and re-render form
        if errors:
            for error in errors:
                messages.error(request, error, extra_tags='danger')
            transaction_type = Transaction.choices
            categories_ls = Category.objects.filter(user=request.user)
            categories_by_type = {}
            for t_value, t_label in transaction_type:
                filtered = categories_ls.filter(category_type=t_value)
                categories_by_type[t_value] = [(c.id, c.category) for c in filtered]
            accounts_ls = Account.objects.filter(user=request.user).values('id','name')
            accounts_select = [(a['id'],a['name']) for a in accounts_ls]
            # Format transaction date for the input field
            date_str = transaction.datetime.strftime('%Y-%m-%dT%H:%M') if transaction.datetime else ''
            # Prepare context for rendering the update form
            context = {
                'id_transaction': id_transaction,  # Transaction ID for reference
                'action': 'Update',                # Action label for the form
                'transaction': transaction,        # Transaction instance to edit
                'date': date_str,                  # Formatted date for input
                'transaction_type': transaction_type, # List of transaction types
                'accounts': accounts_select,       # List of user's accounts
                'categories_by_type': categories_by_type, # Filtered categories by type
            }
            # Render the transaction update form template
            return render(request, "transactions/transactions_form.html", context)
        # Update transaction fields from form data
        transaction.type = type
        transaction.description = description
        transaction.amount = amount
        transaction.origin_account = Account.objects.get(id=account_id) if account_id else None
        if type == 'transfer' and to_account_id:
            transaction.destination_account = Account.objects.get(id=to_account_id)
        else:
            transaction.destination_account = None
        transaction.category = Category.objects.get(id=category_id) if category_id else None
        transaction.datetime = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        transaction.save()
        update_account_balances(type, amount, transaction.origin_account, transaction.destination_account)
        messages.success(request, 'Transaction updated Successfully!')
        return redirect('transactions:transactions_ls')

class TransactionsDeleteView(View):
    def post(self, request, id_transaction):
        transaction = get_object_or_404(Transaction, id=id_transaction)
        update_account_balances(transaction.type, transaction.amount, transaction.origin_account, transaction.destination_account, reverse=True)
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully!')
        return redirect('transactions:transactions_ls')