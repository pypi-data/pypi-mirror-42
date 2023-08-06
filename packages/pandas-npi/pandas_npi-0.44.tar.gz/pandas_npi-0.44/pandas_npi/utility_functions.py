import pandas as pd
import numpy as np

def categorize_type(org_name):
    try:
        np.isnan(org_name)
        return 'provider'
    except:
        return 'facility'
    
def correct_deactivation_date(date, status):
    if status=='active':
        return np.nan
    else:
        return date
    

def extract_nppes_subset(nppes_path='nppes.csv'):

    fields = ['NPI',
              'Entity Type Code',
              'Provider Organization Name (Legal Business Name)',
              'Provider First Name' ,
              'Provider Last Name (Legal Name)',
              'NPI Deactivation Date']

    df_nppes = pd.read_csv(nppes_path, usecols=fields, dtype=str)
    
    df_nppes['nppes_type'] = df_nppes['Provider Organization Name (Legal Business Name)'].apply(lambda x: categorize_type(x))
    df_nppes['nppes_status'] = df_nppes['Entity Type Code'].replace({'1':'active', '2': 'active', np.nan: 'deactivated'})
    df_nppes['NPI Deactivation Date'] = df_nppes.apply(lambda x: correct_deactivation_date(x['NPI Deactivation Date'],x['nppes_status']),axis=1)
    df_nppes = df_nppes.rename({'NPI Deactivation Date': 'nppes_deactivation_date'}, axis=1)
    
    df_nppes['nppes_name'] = df_nppes['Provider Organization Name (Legal Business Name)'].fillna('') + df_nppes['Provider First Name'].fillna('') + " " + df_nppes['Provider Last Name (Legal Name)'].fillna('')
    df_nppes['nppes_name'] = df_nppes['nppes_name'].str.lower()
    df_nppes['nppes_name'] = df_nppes['nppes_name'].apply(lambda x: x.rstrip())
    df_nppes = df_nppes.drop(columns=['Provider Organization Name (Legal Business Name)', 'Provider First Name', 'Provider Last Name (Legal Name)'])

    df_nppes.to_csv('nppes_subset.csv', index=False)
