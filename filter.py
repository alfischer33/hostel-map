import pandas as pd

def with_amenities(hostels, amenity, include_description=True):
  if amenity == '':
    return hostels
  else:
    amenity = amenity.lower()

    if include_description == True:
      have = list(hostels[hostels['description'].str.lower().str.find(amenity.lower()) != -1].index)
    else:
      have = []

    for i, hostel in hostels.iterrows():
      try:
        if i not in have:
          for type in ['free', 'general', 'services', 'food & drink', 'entertainment']:
            for item in hostel[f'{type}_facilities']:
              if item.lower().find(amenity) != -1:
                have.append(i)
                break
      except:
        pass

    return hostels.iloc[have]

def filtered_hostel_df(hostel_df, params):
  
  params_to_function = {
      'name':'',
      'location':'',
      'amenity':'',
      'max_price':100000,
      'min_rating':0,
      'min_reviews':0,
      'max_pop_density':10000000,
      'min_pop_density':0
  }
  
  def update_params(params, params_to_function):
    
    for param in params:
      if param in params_to_function.keys():
        params_to_function[param] = params[param]
    return params_to_function
  
  params_to_function = update_params(params, params_to_function)
  
  
  hostel_df = with_amenities(hostel_df, params_to_function['amenity'])
  hostel_df = hostel_df[hostel_df['name'].str.lower().str.find(params_to_function['name'].lower()) != -1]
  hostel_df = hostel_df[hostel_df['location'].str.lower().str.find(params_to_function['location'].lower()) != -1]
  hostel_df = hostel_df[hostel_df['rating'] >= float(params_to_function['min_rating'])]
  hostel_df = hostel_df[hostel_df['n_reviews'] >= float(params_to_function['min_reviews'])]
  hostel_df = hostel_df[hostel_df['usd_prices_from'] <= float(params_to_function['max_price'])]
  hostel_df = hostel_df[hostel_df['area_pop_density'] <= float(params_to_function['max_pop_density'])]
  hostel_df = hostel_df[hostel_df['area_pop_density'] >= float(params_to_function['min_pop_density'])]
  
  print(f'{len(hostel_df)} hostels returned')
  return hostel_df