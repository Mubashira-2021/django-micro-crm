from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),

    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/add/', views.add_contact, name='add_contact'),
    path('contacts/edit/<int:id>/', views.edit_contact, name='edit_contact'),
    path('contacts/delete/<int:id>/', views.delete_contact, name='delete_contact'),

    # Deals
    path('deals/', views.deal_list, name='deal_list'),
    path('deals/add/', views.add_deal, name='add_deal'),

    # Customers inside deals
    path('deals/<int:deal_id>/customers/add/', views.add_customer, name='add_customer'),

    # Deal edit/delete
    path('deals/edit/<int:id>/', views.edit_deal, name='edit_deal'),
    path('deals/delete/<int:id>/', views.delete_deal, name='delete_deal'),

    # Customer edit/delete
    path('customers/edit/<int:id>/', views.edit_customer, name='edit_customer'),
    path('customers/delete/<int:id>/', views.delete_customer, name='delete_customer'),
]