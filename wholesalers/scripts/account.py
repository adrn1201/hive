import csv
from django_tenants.utils import schema_context 
from products.models import Product, Variation, Category
from wholesalers.models import Domain, Wholesaler
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def create_initial_user():
    superuser = User.objects.create(
        email='hiveorderingsystem@gmail.com',
        username='hiveadmin',
        password=make_password('Hiveadmin_1234'),
        is_superuser=True,
        is_active=True,
        is_staff=True,
        is_wholesaler=True,
        is_retailer=True
    )
    wholesaler = Wholesaler.objects.create(
        user=superuser,
        business_name='Hive',
        schema_name='public',
        barangay='Zone IV',
        address='Zamboanga City',
        contact_name='Hive',
        contact_number='09178907568',
        is_active=True,
        wholesaler_image='logo/hive.png',
        color='orange'
    )
    domain = Domain()
    domain.domain = 'localhost'
    domain.tenant = wholesaler
    domain.is_primary = True
    domain.save()
    
    
def create_user_object(email, username, password):
    return User.objects.create(
        email=email,
        username=username,
        password=make_password(password),
        is_wholesaler=True
    )


def create_wholesaler_object(user, business_name, schema_name, barangay, address, contact_name, contact_number, is_active, wholesaler_image, color):
    return Wholesaler.objects.create(
        user=user,
        business_name=business_name,
        schema_name=schema_name,
        barangay=barangay,
        address=address,
        contact_name=contact_name,
        contact_number=contact_number,
        is_active=is_active,
        wholesaler_image=wholesaler_image,
        color=color
    )


def create_domain_object(test, test1): 
    domain = Domain()
    domain.domain = test
    domain.tenant = test1
    domain.is_primary = True
    domain.save()


def save_user_in_schema(name_of_schema, user_obj):
     with schema_context(name_of_schema):
            user_obj.save()


def read_and_create(filename_prods, schema_name, filename_var, wholesaler, category_name):
    filepath1 = os.path.join(BASE_DIR, filename_prods)
    filepath2 = os.path.join(BASE_DIR, filename_var)
    with open(filepath1, newline='', mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    for row in rows:
        category = ''
        is_variation = ''
        if row['with_variation'] == '0':
            is_variation = False
        elif row['with_variation'] == '1':
            is_variation = True

        with schema_context(schema_name):
            if wholesaler.category_set.count():
                category = wholesaler.category_set.get(id=str(row['category_id']))
            else:
                category = Category.objects.create(
                    id=str(row['category_id']),
                    name=category_name,
                    wholesaler=wholesaler
                )
            Product.objects.create(
                wholesaler=wholesaler,
                category=category,
                product_name=row['product_name'],
                actual_stocks=row['actual_stocks'],
                tempo_stocks=row['tempo_stocks'],
                price=float(row['price']),
                with_variation=is_variation,
                sold=int(row['sold']),
                description=str(row['description']),
                min_orders=int(row['min_orders']),
                product_image=str(row['product_image']),
                created=row['created'],
                id=str(row['id'])
            )
    
    try:    
        with open(filepath2, newline='', mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            
            for row in rows:
                with schema_context(schema_name):
                    product = Product.objects.get(id=row['product_id'])
                    Variation.objects.create(
                        product=product,
                        name=row['name'],
                        actual_stocks_var=int(row['actual_stocks_var']),
                        tempo_stocks_var=int(row['tempo_stocks_var']),
                        created=row['created'],
                        id=str(row['id'])
                    )
    except:
        pass
 
            
def create_hiluck_trading():
    user1 = create_user_object('carlosadrian.catindig@benilde.edu.ph', 'hiluck', 'Wholesaler_12345')

    hiluck = create_wholesaler_object(
        user1,
        'Hiluck Trading',
        'hiluck-trading',
        'ZoneIV',
        'Almonte St',
        'John Doe',
        '09065484520',
        True,
        'logo/hiluck.jpg',
        '#cc0000'
    )
    save_user_in_schema(hiluck.schema_name, user1)
    create_domain_object('hiluck-trading.localhost', hiluck)
    read_and_create('hiluck_products_list.csv', hiluck.schema_name, 'hiluck_withvar.csv', hiluck, 'Kitchenware')
    

def create_rsd_enterprises():
    user2 = create_user_object('juancarlo.nepomuceno@benilde.edu.ph', 'rsd', 'Wholesaler_12345')

    rsd = create_wholesaler_object(
        user2,
        'RSD Enterprises',
        'rsd-enterprises',
        'Zone II',
        'Lim Avenue',
        'Juan Dela Cruz',
        '09065353276',
        True,
        'logo/rsd.png',
        '#ff471a'
    )
    save_user_in_schema(rsd.schema_name, user2)
    create_domain_object('rsd-enterprises.localhost', rsd)
    read_and_create('rsd_products_list.csv', rsd.schema_name, 'rsd_withvar.csv', rsd, 'Electronics')
    

def create_rns_variety_store():
    user3 = create_user_object('janvincentcarlo.dizon@benilde.edu.ph', 'rnsvariety', 'Wholesaler_12345')

    rns = create_wholesaler_object(
        user3,
        'RNS Variety Store',
        'rns-variety-store',
        'Zone II',
        'Lim Avenue',
        'Warren Buffet',
        '09178649752',
        True,
        'logo/rns.jpg',
        '#990000'
    )
    save_user_in_schema(rns.schema_name, user3)
    create_domain_object('rns-variety-store.localhost', rns)
    read_and_create('rns_products_list.csv', rns.schema_name, 'rns_withvar.csv', rns, 'Beverages')
  
      
def create_exbud_consumer_goods_trading():
    user4 = create_user_object('darrenjustin.wu@benilde.edu.ph', 'exbud', 'Wholesaler_12345')

    exbud = create_wholesaler_object(
        user4,
        'EXBUD Consumer Goods Trading',
        'exbud-consumer-goods-trading',
        'Sta. Maria',
        'Veteranz Ave. Ext.',
        'Elon Musk',
        '09063752945',
        True,
        'logo/exbud.jpg',
        '#b38f00'
    )
    save_user_in_schema(exbud.schema_name, user4)
    create_domain_object('exbud-consumer-goods-trading.localhost', exbud)
    read_and_create('exbud_products_list.csv', exbud.schema_name, 'exbud_withvar.csv', exbud, 'Cosmetics')


def create_seven_star():
    user5 = create_user_object('djangodevpy@gmail.com', 'sevenstar', 'Wholesaler_12345')

    seven_star = create_wholesaler_object(
        user5,
        'Seven Star',
        'seven-star',
        'Sta. Maria',
        'Veteranz Ave. Ext.',
        'Steve Harvey',
        '09174595945',
        True,
        'logo/hive.png',
        '#009933'
    )
    save_user_in_schema(seven_star.schema_name, user5)
    create_domain_object('seven-star.localhost', seven_star)
    read_and_create('seven_star_products_list.csv', seven_star.schema_name, 'seven_star_withvar.csv', seven_star, 'Appliances')


create_initial_user()
create_hiluck_trading()
create_rsd_enterprises()
create_rns_variety_store()
create_exbud_consumer_goods_trading()
create_seven_star()

print('Superuser created')
print('Hiluck Trading created')
print('RSD Enterprises created')
print('RNS Variety created')
print('EXBUD Consumer Goods Trading created')
print('Seven Star created')



