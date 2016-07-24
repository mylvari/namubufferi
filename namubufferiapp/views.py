from django.shortcuts import render, get_object_or_404, redirect
from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.template.loader import render_to_string

from models import UserProfile, Product, Category, Transaction
from forms import MoneyForm


# TODO: Create custom context processor to reduce context copy pasting

@login_required
def home_view(request):
    if request.user.is_superuser:
        return render(request, 'namubufferiapp/base_admin.html')
    else:
        context = dict(money_form=MoneyForm(),
                       products=Product.objects.all(),
                       categories=Category.objects.all(),
                       transactions=request.user.userprofile.transaction_set.all(),
                       message="",
                       )

    return render(request, 'namubufferiapp/base_home.html', context)


@login_required
def buy_view(request):
    if request.user.is_superuser:
        return render(request, 'namubufferiapp/base_admin.html')
    context = dict(money_form=MoneyForm(),
                   products=Product.objects.all(),
                   categories=Category.objects.all(),
                   transactions=request.user.userprofile.transaction_set.all(),
                   message="",
                   )

    product = get_object_or_404(Product, pk=request.POST['product_key'])
    price = product.price
    request.user.userprofile.make_payment(price)

    new_transaction = Transaction()
    new_transaction.customer = request.user.userprofile
    new_transaction.amount = -price
    new_transaction.product = product
    new_transaction.save()

    product.make_sale()
    context['receipt'] = new_transaction

    receipt = {'customer': new_transaction.customer.user.username,
               'amount': new_transaction.amount,
               'product': new_transaction.product.name,
               'amount': new_transaction.amount,
               }
    return JsonResponse({'balance': request.user.userprofile.balance,
                         'receipt': render_to_string('namubufferiapp/receipt.html', context)})

    #return render(request, 'namubufferiapp/receipt.html', context)


@login_required
def deposit_view(request):
    if request.user.is_superuser:
        return render(request, 'namubufferiapp/base_admin.html')
    context = dict(money_form=MoneyForm(),
                   products=Product.objects.all(),
                   categories=Category.objects.all(),
                   transactions=request.user.userprofile.transaction_set.all(),
                   message="",
                   )

    if request.method == 'POST':
        money_form = MoneyForm(request.POST)
        if money_form.is_valid():
            amount = request.POST['amount']
            request.user.userprofile.make_deposit(amount)

            new_transaction = Transaction()
            new_transaction.customer = request.user.userprofile
            new_transaction.amount = amount
            new_transaction.save()

            return redirect('/receipt/' + str(new_transaction.pk))
        else:
            context['money_form'] = money_form

    return render(request, 'namubufferiapp/base_home.html', context)


def register_view(request):
    """
    Check for further dev:
    http://www.djangobook.com/en/2.0/chapter14.html
    http://ipasic.com/article/user-registration-and-email-confirmation-django/
    https://docs.djangoproject.com/en/1.7/topics/email/

    """
    context = dict(form=AuthenticationForm(),
                   register_form=UserCreationForm(),
                   message="",
                   )

    if request.method == 'POST':
        register_form = UserCreationForm(request.POST)
        context['register_form'] = register_form
        if register_form.is_valid():
            new_user = register_form.save()

            new_profile = UserProfile()
            new_profile.user = new_user
            new_profile.save()
            context['message'] = 'Register Success. You can now sign in.'

    return render(request, 'namubufferiapp/base_login.html', context)


@login_required
def cancel_transaction_view(request):
    if request.user.is_superuser:
        return render(request, 'namubufferiapp/base_admin.html')
    context = dict(money_form=MoneyForm(),
                   products=Product.objects.all(),
                   categories=Category.objects.all(),
                   transactions=request.user.userprofile.transaction_set.all(),
                   message="",
                   )

    transaction = get_object_or_404(Transaction, pk=request.POST['transaction_key'])

    if (request.user == transaction.customer.user and not transaction.canceled):
        transaction.cancel()
        context['message'] = "Transaction canceled"
        return render(request, 'namubufferiapp/base_home.html', context)

    else:
        return redirect('/')


@login_required
def receipt_view(request, transaction_key):
    if request.user.is_superuser:
        return render(request, 'namubufferiapp/base_admin.html')
    context = dict(money_form=MoneyForm(),
                   products=Product.objects.all(),
                   categories=Category.objects.all(),
                   transactions=request.user.userprofile.transaction_set.all(),
                   message="",
                   )

    print transaction_key
    transaction = get_object_or_404(Transaction, pk=transaction_key)
    context['receipt'] = transaction

    return render(request, 'namubufferiapp/receipt.html', context)
