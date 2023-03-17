import os
import csv
import random
from django_tenants.utils import schema_context
from products.models import Product, Variation
from wholesalers.models import Wholesaler
from orders.models import Order, OrderItem
from django.contrib.auth.models import User 
from django.contrib.auth.hashers import make_password
from retailers.models import Retailer
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def create_user_object(email, username, password, schema_obj):
    user = User.objects.create(
            email=email,
            username=username,
            password=make_password(password),
            is_retailer=True
        )
    with schema_context(schema_obj): 
        user.save()


def create_retailers(filename, schema_obj):
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, newline='', mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        with schema_context(schema_obj):
            users_obj = User.objects.filter(is_retailer=True)
            users = list(users_obj)
            for i in range(len(rows)):
                active=''
                if rows[i]['is_active'] == '0':
                    active = False
                elif rows[i]['is_active'] == '1':
                    active = True
                wholesaler = Wholesaler.objects.get(id=rows[i]['wholesaler_id'])
                Retailer.objects.create(
                    business_name=rows[i]['business_name'],
                    address=rows[i]['address'],
                    contact_name=rows[i]['contact_name'],
                    contact_number=rows[i]['contact_number'],
                    created=rows[i]['created'],
                    wholesaler=wholesaler,
                    retailer_image=rows[i]['retailer_image'],
                    city=rows[i]['city'],
                    region=rows[i]['region'],
                    barangay=rows[i]['barangay'],
                    is_active=active,
                    user=users[i]
                )


def create_orders(filename, wholesaler_obj, schema_obj):
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, newline='', mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        
        for row in rows:
            is_success = ''
            received = ''
            if row['success'] == '0':
                is_success = False
            elif row['success'] == '1':
                is_success = True
            
            if row['is_received'] == '0':
                received = False
            elif row['is_received'] == '1':
                received = True       
            with schema_context(schema_obj):
                retailers = Retailer.objects.all()
                retailer = random.choice(list(retailers))
                order = Order.objects.create(
                    user=retailer.user,
                    wholesaler=wholesaler_obj,
                    reference_number=row['reference_number'],
                    business_name=retailer.business_name,
                    address=row['address'],
                    total_paid=row['total_paid'],
                    mode_of_payment=row['mode_of_payment'],
                    success=is_success,
                    status=row['status'],
                    is_received=received
                )
                order.created = row['created']
                order.save()
                print('order record created')


def create_order_items(filename, schema_obj):          
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, newline='', mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        with schema_context(schema_obj):
            order_objs = Order.objects.all().order_by('id')
            orders = list(order_objs)
            for i in range(len(rows)):
                print(rows[i]['variation_id'])
                variation_obj = ''
                product_obj = Product.objects.get(id=str(rows[i]['product_id']))
                if rows[i]['variation_id'] == '':
                    OrderItem.objects.create(
                        order=orders[i],
                        product=product_obj,
                        price=rows[i]['price'],
                        quantity=rows[i]['quantity']
                    )
                elif rows[i]['variation_id'] != '':
                    variation_obj = product_obj.variation_set.get(id=str(rows[i]['variation_id']))
                    OrderItem.objects.create(
                        order=orders[i],
                        product=product_obj,
                        variation=variation_obj,
                        price=rows[i]['price'],
                        quantity=rows[i]['quantity']
                    )
                print('order item record created')


def create_hiluck_orders():
    emails = ['LevisStar123@gmail.com', 'darrenwu77@gmail.com', 'jvcld26@gmail.com', 'nepomuceno.juancarlo@gmail.com']
    usernames = ['levis', 'darren_hiluck', 'jan_hiluck', 'jc_hiluck']
    hiluck = Wholesaler.objects.get(id=2)
    for i in range(len(emails)):
        create_user_object(emails[i], usernames[i], 'Retailer@12345', hiluck.schema_name)

    create_retailers('hiluck_retailer.csv', hiluck.schema_name)
    create_orders('hiluck_orders.csv', hiluck, hiluck.schema_name)
    create_order_items('hiluck_order_items.csv', hiluck.schema_name)    
    
    
def create_rsd_orders():
    emails = ['NRWMarketing8@gmail.com', 'darrenwu77@gmail.com', 'jvcld26@gmail.com', 'nepomuceno.juancarlo@gmail.com']
    usernames = ['nrw', 'darren_rsd', 'jan_rsd', 'jc_rsd']
    rsd = Wholesaler.objects.get(id=3)
    for i in range(len(emails)):
        create_user_object(emails[i], usernames[i], 'Retailer@12345', rsd.schema_name)

    create_retailers('rsd_retailer.csv', rsd.schema_name)
    create_orders('rsd_orders.csv', rsd, rsd.schema_name)
    create_order_items('rsd_order_items.csv', rsd.schema_name)    


def create_rns_orders():
    emails = ['darrenwu77@gmail.com', 'Powerrace888@gmail.com', 'jvcld26@gmail.com', 'nepomuceno.juancarlo@gmail.com']
    usernames = ['darren_rns', 'powerace', 'jan_rns', 'jc_rns']
    rns = Wholesaler.objects.get(id=4)
    for i in range(len(emails)):
        create_user_object(emails[i], usernames[i], 'Retailer@12345', rns.schema_name)

    create_retailers('rns_retailer.csv', rns.schema_name)
    create_orders('rns_orders.csv', rns, rns.schema_name)
    create_order_items('rns_order_items.csv', rns.schema_name)    


def create_exbud_orders():
    emails = ['FiveStar8123@gmail.com', 'darrenwu77@gmail.com', 'jvcld26@gmail.com', 'nepomuceno.juancarlo@gmail.com']
    usernames = ['fivestar', 'darren_exbud', 'jan_exbud', 'jc_exbud']
    exbud = Wholesaler.objects.get(id=5)
    for i in range(len(emails)):
        create_user_object(emails[i], usernames[i], 'Retailer@12345', exbud.schema_name)

    create_retailers('exbud_retailer.csv', exbud.schema_name)
    create_orders('exbud_orders.csv', exbud, exbud.schema_name)
    create_order_items('exbud_order_items.csv', exbud.schema_name)    


def create_seven_orders():
    emails = ['darrenwu77@gmail.com', 'jvcld26@gmail.com', 'nepomuceno.juancarlo@gmail.com']
    usernames = ['darren_seven', 'jan_seven', 'jc_seven']
    seven = Wholesaler.objects.get(id=6)
    for i in range(len(emails)):
        create_user_object(emails[i], usernames[i], 'Retailer@12345', seven.schema_name)

    create_retailers('seven_retailer.csv', seven.schema_name)
    create_orders('seven_orders.csv', seven, seven.schema_name)
    create_order_items('seven_order_items.csv', seven.schema_name)    
    
    
create_hiluck_orders()
create_rsd_orders()
create_rns_orders()
create_exbud_orders()
create_seven_orders()
print('Hiluck User records created')
print('Hiluck retailer records created')
print('Hiluck order records created')
print('Hiluck order item records created')
print('RSD User records created')
print('RSD retailer records created')
print('RSD order records created')
print('RSD order item records created')
print('RNS User records created')
print('RNS retailer records created')
print('RNS order records created')
print('RNS order item records created')
print('Exbud User records created')
print('Exbud retailer records created')
print('Exbud order records created')
print('Exbud order item records created')

