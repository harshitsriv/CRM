from django.db.models.signals import post_save
from .models import Customer
from django.contrib.auth.models import User, Group


def customer_profile(sender, instance, created, **kwargs):
    if created :
        group = Group.objects.get(name = 'customer')   # to automatically attach group of customer to newly added user
        instance.groups.add(group)
        Customer.objects.create(   
            user = instance,
            name = instance.username,
        )# to automatically create a customer for a new user
        print('Profile Created !!')


post_save.connect(customer_profile , sender  = User)
''' Notes:
    need to override app.py ready method to get signals working

'''