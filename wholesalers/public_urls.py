from django.contrib import admin

from .models import Wholesaler, Domain

tenant = Wholesaler(
                schema_name = 'public',
                business_name = 'hive',
                address = '4',
                contact_name='Darren',
                contact_number='091735352723',
                is_active=True
                )
tenant.save()

# Add one or more domains for the tenant
domain = Domain()
domain.domain = 'hive.localhost' # don't add your port or www here! on a local server you'll want to use localhost here
domain.tenant = tenant
domain.is_primary = True
domain.save()
# tenant = Empresa(domain_url = 'titu.kinetfood.local',
#                 schema_name = 'titu',
#                 nombre = 'Titu Cocktail Xpress',
#                 nro_mesas = '4',
#                 )
# tenant.save()

# tenant = Empresa(domain_url = 'lasalva.kinetfood.local',
#                 schema_name = 'lasalva',
#                 nombre = 'La Salva burguer',
#                 nro_mesas = '10',
#                 )
# tenant.save()
