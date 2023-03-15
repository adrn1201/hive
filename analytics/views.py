from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import pandas as pd
from joblib import load
import json
import datetime
from products.models import Product
from products.utils import search_products, paginate_products
from wholesalers.models import Domain, Wholesaler
from django_tenants.utils import remove_www
import os
from django.conf import settings

@login_required(login_url='login_wholesaler')
def display_analytics(request):
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
        
    num_days = 14
    num_months = 6
    is_predict = False
    product_id = ''
    labels = []
    data = []
    forecasted_demand = ''
    variation = ''
    context = {}
    products, search_query = search_products(request)
    custom_range, products = paginate_products(request, products, 10)
    predict_products = None
    new_product = False
    unit = ''

    try:
        pickle_file_path = os.path.join(settings.BASE_DIR, f'{wholesaler.business_name}_xgboost.pkl')
        columns_file_path = os.path.join(settings.BASE_DIR, f'{wholesaler.business_name}_columns.pkl')
        
        model = load(pickle_file_path)
        columns = load(columns_file_path)
    except:
        return render(request, 'analytics/message.html') 
    
     
    if(request.GET.get('predict')): 
        is_predict = True
        new_product = False
        product_id = request.GET.get('predict')
        predict_products = Product.objects.filter(id=str(product_id))

        for prod in predict_products:
            prod.analytics_date = datetime.date.today()
            prod.save()
      
        product_data = pd.DataFrame(list(predict_products.values()))

        product_data['date'] = pd.to_datetime(product_data['analytics_date'])
        product_data['day_of_week'] = product_data['date'].dt.dayofweek
        product_data['month'] = product_data['date'].dt.month
        product_data['year'] = product_data['date'].dt.year

        test_data = product_data.iloc[-num_days:]
        next_date = pd.date_range(test_data['date'].max(), periods=num_days+1, freq='D')[1:]
        if request.GET.get('period') and request.GET.get('period') == 'monthly':
            unit = 'month'
            test_data = product_data.iloc[-num_months:] 
            next_date = pd.date_range(test_data['date'].max(), periods=num_months+1, freq='MS')[1:] 
        else:
            unit = 'day'
            test_data = product_data.iloc[-num_days:]
            next_date = pd.date_range(test_data['date'].max(), periods=num_days+1, freq='D')[1:]

       
    
        predictor_data = {}
        
        ids = [k.split('id_')[1] for k in columns if len(k.split('id_')) > 1]

        if request.GET.get('predict') in ids:
            for i in columns:
                if i != 'year' and i != 'month' and i != 'dayofweek':
                    if len(i.split('id_')) > 1 and i.split('id_')[1] == request.GET.get('predict'):
                        predictor_data[i] = 1                    
                    else:
                        predictor_data[i] = 0
                    
                    if predict_products[0].with_variation:
                        if request.GET.get('variationId') and (len(i.split('id_')) > 1 and i.split('id_')[1] == request.GET.get('variationId')):
                            predictor_data[i] = 1    
                            variation = predict_products[0].variation_set.get(id=request.GET.get('variationId'))
                    else:
                        if len(i.split('id_')) > 1 and i.split('id_')[1] == '/n':
                            predictor_data[i] = 1
                              
                elif i ==  'year':
                    predictor_data[i] = next_date.year
                elif i == 'month':
                    predictor_data[i] = next_date.month
                elif i == 'dayofweek':
                    predictor_data[i] = next_date.dayofweek
        else:
            new_product = True
            context = {
               'is_predict':is_predict,
               'new_product':new_product,
               'product': predict_products[0],
               'variation':variation,
               'products':products, 
               'custom_range':custom_range,
               'search_query':search_query
            }
            return render(request, 'analytics/forecasting.html', context)
        
        next_date_df = pd.DataFrame(predictor_data)
                
        X_next_date = next_date_df
        y_next_date = model.predict(X_next_date)

        predicted_demand = []
        forecasted_demand = []
        
        forecasted_date = list(next_date.strftime('%Y-%m-%d'))
        
        for i in y_next_date:
            predicted_demand.append(int(i))

        for i in range(len(forecasted_date)):
            forecasted_demand.append({'date': datetime.datetime.strptime(forecasted_date[i], "%Y-%m-%d").date(), 'demand':predicted_demand[i]})
            
        labels = json.dumps(forecasted_date)
        data = json.dumps(predicted_demand)
        

    if predict_products != None:
        predict_products = predict_products[0]
    else:
        predict_products = None
    
    context = {
               'is_predict':is_predict,
               'new_product':new_product,
               'labels':labels,
               'unit':unit, 
               'product': predict_products,
               'variation':variation,
               'data': data, 
               'forecasted_demand':forecasted_demand, 
               'products':products, 
               'custom_range':custom_range,
               'search_query':search_query
            }
    return render(request, 'analytics/forecasting.html', context)

