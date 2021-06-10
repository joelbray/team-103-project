# Works for the following census table: SELECTED CHARACTERISTICS OF THE NATIVE AND FOREIGN-BORN POPULATIONS
# from uszipcode import SearchEngine, SimpleZipcode

import uszipcode
import pandas as pd

class DataSource:
    def __init__(self, meta_file=None, data_file=None):
        self.meta_file = meta_file
        self.data_file = data_file
        self.data = None
    
    def get_data(self):

        if self.meta_file is None or self.data_file is None:
            return None
        # if data is read already, it wont read it again
        if self.data:
            return self.data
        
        # used to get the zip data

        search = uszipcode.SearchEngine()
        
        # read the files
        _ , ext = self.meta_file.split('.')
        if ext == 'csv':
            meta = pd.read_csv(self.meta_file)
        elif ext == 'xlsx':
            meta = pd.read_excel(self.meta_file)
        else:
            print('Extension {0} is not supported'.format(ext))
            return None
        
        _ , ext = self.data_file.split('.')
        if ext == 'csv':
            data = pd.read_csv(self.data_file)
        elif ext == 'xlsx':
            data = pd.read_excel(self.data_file)
        else:
            print('Extension {0} is not supported'.format(ext))
            return None
        
        data = data.drop(index=0)
        

        self.col_dict = {g:i for g,i in zip(meta['GEO_ID'][1:].to_list(),meta['id'][1:].to_list())}

        # get city and state to then query
        # add that info to the dataframe (data)
        city,state = data['NAME'][1].split(',')
        city = city.rstrip('city').strip() 
        # res = search.by_city_and_state(city,state)
        res = []

        # get the zip codes then add to dataframe (data)
        zips = ','.join([z.zipcode for z in res])
        data['zip_codes'] = [zips]
            
        self.data = data
        
        return data
    
    # function to change column names
    def change_col_name(self):
        if self.data is None:
            print('Data sources not given')
            return None
        self.data.columns = self.data.columns[:2].to_list() + list(self.col_dict.values()) + ['zip_codes']
        return self.data

    # get dictionary to translate col names
    def get_dict(self):
        if self.data is None:
            print('Data sources not given')
            return None
        return self.col_dict
