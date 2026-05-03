from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import pandas as pd
import numpy as np
from .models import Deal, Customer, Contact
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm']:
            User.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password']
            )
            return redirect('login')
    return render(request, 'register.html')


def dashboard(request):
    contacts = Contact.objects.filter(owner=request.user).values()
    deals = Deal.objects.filter(owner=request.user).values()
    customers = Customer.objects.all().values()

    # Convert to DataFrame
    df_contacts = pd.DataFrame(contacts)
    df_deals = pd.DataFrame(deals)
    df_customers = pd.DataFrame(customers)

    total_contacts = len(df_contacts)
    total_deals = len(df_deals)

    if not df_customers.empty:
        hot = df_customers[df_customers['lead_status'] == 'Hot'].shape[0]
        warm = df_customers[df_customers['lead_status'] == 'Warm'].shape[0]
        cold = df_customers[df_customers['lead_status'] == 'Cold'].shape[0]

        # NumPy example
        avg_leads = np.mean([hot, warm, cold])
    else:
        hot = warm = cold = avg_leads = 0

    deals_qs = Deal.objects.filter(owner=request.user)

    deal_names = []
    deal_counts = []

    for d in deals_qs:
        deal_names.append(d.title)
        deal_counts.append(
            Customer.objects.filter(deal=d).count()
        )

    return render(request, 'dashboard.html', {
        'contacts': total_contacts,
        'deals': total_deals,
        'hot': hot,
        'warm': warm,
        'cold': cold,
        'avg': avg_leads,
        'deal_names': deal_names,
        'deal_counts': deal_counts
    })


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def contact_list(request):

    view_type = request.GET.get('view', 'my')  # default = my
    query = request.GET.get('q')

    if view_type == 'all':
        contacts = Contact.objects.all()
    else:
        contacts = Contact.objects.filter(owner=request.user)

    if query:
        contacts = contacts.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query)
        )

    return render(request, 'contacts/list.html', {
        'contacts': contacts,
        'view_type': view_type
    })


@login_required
def add_contact(request):
    if request.method == 'POST':
        Contact.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            owner=request.user
        )
        return redirect('contact_list')

    return render(request, 'contacts/add.html')


@login_required
def edit_contact(request, id):
    contact = Contact.objects.get(id=id)

    if request.method == 'POST':
        contact.name = request.POST['name']
        contact.email = request.POST['email']
        contact.save()
        return redirect('contact_list')

    return render(request, 'contacts/edit.html', {'contact': contact})


@login_required
def delete_contact(request, id):
    contact = Contact.objects.get(id=id)
    contact.delete()
    return redirect('contact_list')

@login_required
def contact_view(request, id):
    contact = Contact.objects.get(id=id)
    return render(request, 'contacts/view.html', {'contact': contact})

@login_required
def deal_list(request):
    deals = Deal.objects.filter(owner=request.user)

    deal_data = []

    for deal in deals:
        customers = Customer.objects.filter(deal=deal)

        deal_data.append({
            'deal': deal,
            'customers': customers
        })

    return render(request, 'deals/list.html', {
        'deal_data': deal_data
    })


@login_required
def add_deal(request):
    if request.method == 'POST':
        Deal.objects.create(
            title=request.POST['title'],
            owner=request.user
        )
        return redirect('deal_list')

    return render(request, 'deals/add.html')


@login_required
def add_customer(request, deal_id):
    deal = Deal.objects.get(id=deal_id)
    contacts = Contact.objects.filter(owner=request.user)

    if request.method == 'POST':
        Customer.objects.create(
            contact_id=request.POST['contact'],
            deal=deal,
            lead_status=request.POST['status']
        )
        return redirect('deal_list')

    return render(request, 'deals/add_customer.html', {
        'contacts': contacts,
        'deal': deal
    })

# EDIT DEAL
@login_required
def edit_deal(request, id):
    deal = get_object_or_404(Deal, id=id, owner=request.user)

    if request.method == 'POST':
        deal.title = request.POST['title']
        deal.save()
        return redirect('deal_list')

    return render(request, 'deals/edit_deal.html', {'deal': deal})


# DELETE DEAL
@login_required
def delete_deal(request, id):
    deal = get_object_or_404(Deal, id=id, owner=request.user)
    deal.delete()
    return redirect('deal_list')


# EDIT CUSTOMER
@login_required
def edit_customer(request, id):
    customer = get_object_or_404(Customer, id=id)

    if request.method == 'POST':
        customer.lead_status = request.POST['status']
        customer.save()
        return redirect('deal_list')

    return render(request, 'deals/edit_customer.html', {'customer': customer})


# DELETE CUSTOMER
@login_required
def delete_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    customer.delete()
    return redirect('deal_list')