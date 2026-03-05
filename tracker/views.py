from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Transaction, Category
from .forms import TransactionForm, CategoryForm
from django.db.models import Sum
from django.utils.timezone import now

@login_required
def home(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    # Filter by category or month if GET parameters are present
    category_id = request.GET.get('category')
    month = request.GET.get('month')

    if category_id and category_id != 'all':
        transactions = transactions.filter(category_id=category_id)

    if month and month != 'all':
        transactions = transactions.filter(date__month=int(month))

    total_income = sum(t.amount for t in transactions if t.transaction_type == 'income')
    total_expense = sum(t.amount for t in transactions if t.transaction_type == 'expense')
    balance = total_income - total_expense

    # Prepare category chart data (only expense)
    expense_transactions = transactions.filter(transaction_type='expense')
    category_values_dict = expense_transactions.values('category__name').annotate(total=Sum('amount'))
    category_labels = [c['category__name'] for c in category_values_dict]
    category_values = [c['total'] for c in category_values_dict]

    # All categories for filter dropdown
    all_categories = Category.objects.filter(user=request.user)

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'category_labels': category_labels,
        'category_values': category_values,
        'all_categories': all_categories,
        'selected_category': category_id or 'all',
        'selected_month': month or 'all',
    }
    return render(request, 'tracker/home.html', context)
@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('home')
    else:
        form = TransactionForm()
    return render(request, 'tracker/add_transaction.html', {'form': form})


@login_required
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'tracker/edit_transaction.html', {'form': form})


@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('home')
    return render(request, 'tracker/delete_transaction.html', {'transaction': transaction})


@login_required
def manage_categories(request):
    categories = Category.objects.filter(user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('manage_categories')
    else:
        form = CategoryForm()
    return render(request, 'tracker/manage_categories.html', {'categories': categories, 'form': form})
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})