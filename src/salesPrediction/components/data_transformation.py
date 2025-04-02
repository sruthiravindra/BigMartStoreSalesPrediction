import os
from salesPrediction import logger
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split
import pandas as pd
from salesPrediction.config.configuration import DataTransformationConfig
import json

class DataTransformation:
    def __init__(self, config:DataTransformationConfig):
        self.config = config
        # we already have train and test data set in the resources folder, we only need to copy them 
        self.train_data = pd.read_csv(self.config.train_data_path)
        self.test_data = pd.read_csv(self.config.test_data_path)
    
    def train_test_splitting(self):
        
        print(self.train_data.isna().sum())
        self.train_data.to_csv(os.path.join(self.config.data_path, "Train.csv"), index=False)
        self.test_data.to_csv(os.path.join(self.config.data_path, "Test.csv"), index= False)

        logger.info("Completed saving train and test data to transformation folder")
        logger.info(self.train_data.shape)
        logger.info(self.test_data.shape)

        print(self.train_data.shape)
        print(self.test_data.shape)
    
    def convert_column_datatype(self):
        try:

            with open(self.config.mismatch_data_type_path, "r") as f:
                mismatched_cols =  json.loads(f.read())

            # convert train dataset
            data = pd.read_csv(self.config.train_data_path)
            for col, dtype_info in mismatched_cols.items():
                if dtype_info["expected"] == "string":
                    self.train_data[col] = self.train_data[col].astype("string")
                    logger.info(f"Converted data type of column {col} to {dtype_info['expected']}")

            # convert test dataset
            data = pd.read_csv(self.config.test_data_path)
            for col, dtype_info in mismatched_cols.items():
                if dtype_info["expected"] == "string":
                    self.test_data[col] = self.test_data[col].astype("string")
                    logger.info(f"Converted data type of column {col} to {dtype_info['expected']}")

        except Exception as e:
            raise e
        
    def clean_data(self):

        logger.info(f"Start cleaning training data")
        df = self.train_data
        df = self.__clean_categorical_features(df)
        df = self.__handle_outlet_size_missing_values(df)
        df = self.__handle_item_weight_missing_values(df)
        df = self.__encode_binary_features(df)
        self.train_data = df
        logger.info(f"Completed cleaning training data")

    
    def __clean_categorical_features(self, df):
        """Standardize categorical column values before encoding."""
        df['Item_Fat_Content'] = df['Item_Fat_Content'].replace({
            'low fat': 'Low Fat',
            'LF': 'Low Fat',
            'reg': 'Regular'
        })
        return df
    
    def __group_item_type(self, item):
        """
        Group similar item types 
        """

        if item in ['Dairy', 'Meat', 'Seafood']:
                return 'Perishable'
        elif item in ['Fruits and Vegetables', 'Breads', 'Breakfast', 'Starchy Foods']:
            return 'Fresh'
        elif item in ['Frozen Foods', 'Canned']:
            return 'Processed'
        elif item in ['Soft Drinks', 'Hard Drinks']:
            return 'Beverages'
        elif item in ['Health and Hygiene', 'Household']:
            return 'Non-Food'
        elif item in ['Baking Goods', 'Snack Foods']:
            return 'Packaged'
        else:
            return 'Other'
        
    def __handle_outlet_size_missing_values(self, df):
        """
        The values have been handled by carefully checking the relationship between the outlet_type, outlet_size and outlet_location_type

        It was observed that all rows with outlet_type='grocery' belonged to nan or 'Small', hence all those with nan were set to small
        It was observed that all rows with Outlet_Location_Type = 'Tier 2' and Outlet_Type = 'Supermarket Type1' were either 'Small' or null. hence all those with nan were set to small
        """

        # replace Small for grocery
        df.loc[(df['Outlet_Type'] == 'Grocery Store') & (df['Outlet_Size'].isna()), 'Outlet_Size'] = 'Small'

        # replace Small for Outlet_Location_Type = 'Tier 2' and Outlet_Type = 'Supermarket Type1'
        df.loc[(df['Outlet_Location_Type'] == 'Tier 2') & (df['Outlet_Type'] == 'Supermarket Type1') & (df['Outlet_Size'].isna()), 'Outlet_Size'] = 'Small'
        
        return df

    def __handle_item_weight_missing_values(self,df):
        """
        It was observed that 1463 records had null values in item_weight field

        All these belong to Outlet_Establishment_Year=1985 and all of Outlet_Establishment_Year=1985 have Item_Weight null
        This is a valuable insight because you can impute more intelligently instead of filling with a blanket mean or median.
        """

        # Get list of Item_Identifier values where weight is missing
        df_weight_null = df[df['Item_Weight'].isna()]['Item_Identifier']

        for item_id in df_weight_null:
            # Find the mean weight of this item from outlets not in 1985 and not null
            item_mean = df[(df['Item_Identifier'] == item_id) &
                        (df['Outlet_Establishment_Year'] != 1985) &
                        (df['Item_Weight'].notna())]['Item_Weight'].mean()
            
            # Apply this mean only to rows with missing weights for this item and year = 1985
            df.loc[(df['Item_Identifier'] == item_id) &
                (df['Item_Weight'].isna()) &
                (df['Outlet_Establishment_Year'] == 1985), 'Item_Weight'] = item_mean

        # still 4 records have null value
        # Belong to Item_Identifiers that only exist in Outlet_Establishment_Year == 1985
        # Never had a known weight, so no mean to compute from other outlets

        # Step 1: Fallback by Item_Type
        df['Item_Weight'] = df.groupby('Item_Type')['Item_Weight'].transform(
            lambda x: x.fillna(x.median())
        )

        # Step 2: Final fallback with global median (if any NaNs remain)
        df['Item_Weight'].fillna(df['Item_Weight'].median(), inplace=True)


        return df
    
    def __encode_binary_features(self, df):
        
        df = self.__encode_fat_content(df)
        df = self.__encode_outlet_type(df)
        df = self.__encode_item_type(df)
        df = self.__encode_outlet_size(df)
        df = self.__encode_outlet_location(df)

        return df

    
    def __encode_fat_content(self, df):

        """Apply Label Encoding to binary categorical columns."""
        df['Item_Fat_Content'] = df['Item_Fat_Content'].map({'Low Fat': 0, 'Regular': 1})

        return df
        
    def __encode_outlet_type(self, df):
        """
        Both one hot and label encoding has been performed as at this stage we are not sure what model will be using on this dataset
        """


        """Apply One Hot Encoding """
        o_encoder = OneHotEncoder(handle_unknown="ignore", sparse_output = False)
        encoded_features = o_encoder.fit_transform(df[['Outlet_Type']])

        encoded_df = pd.DataFrame(encoded_features, columns = o_encoder.get_feature_names_out())

        df  = pd.concat([df, encoded_df], axis=1)

        """Apply Label Encoding on Outlet_Type """
        l_encoder = LabelEncoder()
        df['Outlet_Type_LabelEncoded'] = l_encoder.fit_transform(df['Outlet_Type'])
        # df = df.drop(columns=['Outlet_Type'])
        df.head()

        return df
    
    def __encode_item_type(self, df):

        """Apply Feature Reduction and then One Hot Encoding on Item_Type"""
        df['Item_Type_Feature_Encoded'] = df['Item_Type'].apply(self.__group_item_type)
        o_encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        encoded_features = o_encoder.fit_transform(df[['Item_Type_Feature_Encoded']])
        encoded_df = pd.DataFrame(encoded_features, columns=o_encoder.get_feature_names_out())
        df = pd.concat([df,encoded_df], axis=1)

        return df
    
    def __encode_outlet_size(self, df):

        """Apply ordinal encoding to Outlet_Size."""
        size_mapping = {'Small' : 0, 'Medium' : 1, 'High': 2}
        df['Outlet_Size'] = df['Outlet_Size'].map(size_mapping)
        return df
    
    def __encode_outlet_location(self, df):
        """Apply ordinal encoding to Outlet_Location_Type."""
        location_mapping = {'Tier 1': 0, 'Tier 2': 1, 'Tier 3': 2}
        df['Outlet_Location_Type'] = df['Outlet_Location_Type'].map(location_mapping)
        return df