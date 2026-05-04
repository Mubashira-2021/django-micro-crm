from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Deal(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=[
        ('Open', 'Open'),
        ('Won', 'Won'),
        ('Lost', 'Lost')
    ], default='Open')

    expected_close_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Customer(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    lead_status = models.CharField(max_length=10, choices=[
        ('Hot', 'Hot'),
        ('Warm', 'Warm'),
        ('Cold', 'Cold')
    ], default='Cold')

    role = models.CharField(max_length=100, blank=True)  # Decision maker, Influencer

    last_contacted = models.DateField(null=True, blank=True)