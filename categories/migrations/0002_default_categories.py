# Generated by Django 5.2.4 on 2025-07-29 04:09

from django.db import migrations

def add_default_categories(apps, schema_editor):
    category = apps.get_model('categories', 'Category')
    category.objects.create(category='Awards',category_type='income',user=None)
    category.objects.create(category='Coupons', category_type='income', user=None)
    category.objects.create(category='Grants', category_type='income', user=None)
    category.objects.create(category='Lottery', category_type='income', user=None)
    category.objects.create(category='Refunds', category_type='income', user=None)
    category.objects.create(category='Rental', category_type='income', user=None)
    category.objects.create(category='Salary', category_type='income', user=None)
    category.objects.create(category='Sale', category_type='income', user=None)

    category.objects.create(category='Rent', category_type='expense', user=None)
    category.objects.create(category='Bill', category_type='expense', user=None)
    category.objects.create(category='Home', category_type='expense', user=None)
    category.objects.create(category='Groceries', category_type='expense', user=None)
    category.objects.create(category='Utilities', category_type='expense', user=None)
    category.objects.create(category='Transportation', category_type='expense', user=None)
    category.objects.create(category='Insurance', category_type='expense', user=None)
    category.objects.create(category='Healthcare', category_type='expense', user=None)
    category.objects.create(category='Dining Out', category_type='expense', user=None)
    category.objects.create(category='Entertainment', category_type='expense', user=None)
    category.objects.create(category='Clothing', category_type='expense', user=None)
    category.objects.create(category='Education', category_type='expense', user=None)
    category.objects.create(category='Subscriptions', category_type='expense', user=None)
    category.objects.create(category='Phone', category_type='expense', user=None)
    category.objects.create(category='Internet', category_type='expense', user=None)
    category.objects.create(category='Gifts', category_type='expense', user=None)
    category.objects.create(category='Travel', category_type='expense', user=None)
    category.objects.create(category='Childcare', category_type='expense', user=None)
    category.objects.create(category='Pets', category_type='expense', user=None)
    category.objects.create(category='Household Items', category_type='expense', user=None)
    category.objects.create(category='Loan Payments', category_type='expense', user=None)
    category.objects.create(category='Miscellaneous', category_type='expense', user=None)

class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_default_categories),
    ]
