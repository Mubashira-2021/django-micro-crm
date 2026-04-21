from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Deal(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Customer(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)

    lead_status = models.CharField(
        max_length=10,
        choices=[
            ('Hot', 'Hot'),
            ('Warm', 'Warm'),
            ('Cold', 'Cold')
        ]
    )