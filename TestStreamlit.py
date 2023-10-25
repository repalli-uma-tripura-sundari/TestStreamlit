#streamlit run D:\\DDP\\TestStreamlit.py

import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

data = pd.read_csv("D:\\PowerUP\\products.csv")
df = data.copy()
df['Product_Cost_$'] = df['Product_Cost'].str.replace('$','').astype(float)
df['Product_Price_$'] = df['Product_Price'].str.replace('$','').astype(float)
#st.write(df)



data2 = pd.read_csv("D:\\PowerUP\\stores.csv")
#st.write(data2)

data3 = pd.read_csv("D:\\PowerUP\\inventory.csv")
#st.write(data3)

df = df.drop(columns = ['Product_Cost','Product_Price'])
data2 = data2.drop(columns = 'Store_Open_Date')





storesinventory = pd.merge(data2, data3, on = 'Store_ID', how = 'inner')

productsinvetory = pd.merge(df, data3, on = 'Product_ID', how = 'inner')
productsinvetory['Inventory Cost'] = productsinvetory['Product_Cost_$']*productsinvetory['Stock_On_Hand']
productsinvetory['Inventory Price'] = productsinvetory['Product_Price_$']*productsinvetory['Stock_On_Hand']
productsinvetory['Expected Profit'] = productsinvetory['Inventory Price'] - productsinvetory['Inventory Cost']
invetory = productsinvetory.groupby('Product_Name')[['Product_Cost_$',
       'Product_Price_$', 'Stock_On_Hand', 'Inventory Cost',
       'Inventory Price', 'Expected Profit']].sum().reset_index()



def Data():
	st.title("Required Datasets")
	col1, col2 = st.columns(2)
	col1.write('products')
	col1.write(df)
	#col3, col4 = st.columns(2)
	col1.write('stores')
	col1.write(data2)
	col2.write('inventory')
	col2.write(data3)

	
def Sales_Overview():
	st.title("Sales Overview")	
	col1, col2,col3 = st.columns(3)
	col1.write('product performs better in terms of profits')
	col2.write('Revenue and Profit over Months')
	expprft = invetory[['Product_Name','Stock_On_Hand','Expected Profit']]
	col1.write('expected profits from the inventory productsavailable')
	col1.write(expprft)
	
	
	col3.write('inventory cost and expected profits')
	expprft = invetory[['Product_Name','Stock_On_Hand','Expected Profit']]
	
	ProdCat = st.sidebar.selectbox('Product_Category', ['All','Toys', 'Art & Crafts', 'Games', 'Electronics','Sports & Outdoors'])  
	if ProdCat == 'All':
		filtered_data = df  # No filtering applied
	else:
		filtered_data = df[df['Product_Category'] == ProdCat]
		
	
	
	
def main():
	st.sidebar.title("Navigation")
	selectPage = st.sidebar.radio("Go To", ['Data','Sales_Overview'])
	
	if selectPage == 'Data':
		Data()
	if selectPage == 'Sales_Overview':
		Sales_Overview()
main()	