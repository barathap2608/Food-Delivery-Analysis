import pandas as pd
from sqlalchemy import create_engine
import numpy as np
from sqlalchemy import create_engine


data = pd.read_csv(r"C:\Users\acer\OneDrive\文件\python files\ONINE_FOOD_DELIVERY_ANALYSIS (1).csv")
df = pd.DataFrame(data)

df["Customer_Age"].fillna(df["Customer_Age"].mean().astype(int),inplace=True)
df["Customer_Gender"].fillna("Unknown",inplace=True)
df["City"].fillna("Unknown",inplace=True)
df["Area"].fillna("Unknown",inplace=True)
df["Cuisine_Type"].fillna("unknown",inplace=True)
df["Order_Date"].dropna(axis=0,inplace=True)
df["Order_Time"].dropna(axis=0,inplace=True)
df["Delivery_Time_Min"].fillna(df["Delivery_Time_Min"].mean(),inplace=True)
df["Distance_km"].fillna(df["Distance_km"].mean(),inplace=True)
df["Order_Value"].fillna(df["Order_Value"].mean(),inplace=True)
df["Discount_Applied"].fillna(df["Discount_Applied"].mean(),inplace=True)
df["Final_Amount"].fillna(df["Final_Amount"].median(),inplace=True)
df["Payment_Mode"].fillna("Unknown",inplace=True)
df["Cancellation_Reason"].fillna("Unknown",inplace=True)
df["Delivery_Rating"].fillna(np.random.choice(df["Delivery_Rating"].dropna().values),inplace=True)
df["Peak_Hour"].fillna("Unknown",inplace=True)
df['age_group'] = pd.cut(df['Customer_Age'], bins=[18, 25, 35, 45, 55, 60], labels=['Young Adult', 'Adult', 'Middle-Aged', 'Senior Adult', 'Elder'], include_lowest=True)

engine = create_engine('mysql+pymysql://root:12345@localhost:3306/fooddelivery')

df.to_sql('food_delivery_table', con=engine, if_exists='replace', index=False)

engine = create_engine('sqlite:///fooddelivery.db')
df.to_sql('food_delivery_table', con=engine, if_exists='replace', index=False)

