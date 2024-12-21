import pandas as pa
import numpy as na
import matplotlib.pyplot as plt
import os


# Saving multiple csv files in a single file
# Directory containing the CSV files
# folder_path = r'C:\Users\DC\Desktop\Python\FIrst_Project\Sales_data'

# # List all files in the folder
# Files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
# All_Months_Data = pa.DataFrame()

# # Loop through each file, construct the full path, and read the file
# for file in Files:
#     file_path = os.path.join(folder_path, file)  # Correctly combine the folder path and file name
#     df = pa.read_csv(file_path)
#     All_Months_Data = pa.concat([All_Months_Data, df], ignore_index=True)

# # Display the first few rows of the combined DataFrame
# print(All_Months_Data.tail())

# # # Now we will save the All_Months_Data 
# # saved_place = r'C:\Users\DC\Desktop\Python\FIrst_Project\Combined_Sales_Data.csv'
# # All_Months_Data.to_csv(saved_place, index=False)
# # print(f"Combined CSV file saved at: {saved_place}")

# now the file that contains all the files is
all_data = pa.read_csv(r'C:\Users\DC\Desktop\Python\FIrst_Project\Combined_Sales_Data.csv')
# before going to first question we have to clean our data so
NAN = all_data[all_data.isna().any(axis = 1)]
all_data = all_data.dropna(how = 'all')



# first question is what is the best month for the sales?
all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']
all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
all_data['Cities'] = all_data['Purchase Address'].str.split(',').str[1].str.strip()
all_data['States'] = all_data['Purchase Address'].str.split(',').str[2].str.split().str[0]
all_data['Quantity Ordered'] = pa.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pa.to_numeric(all_data['Price Each'])

all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']
# result = all_data.groupby('Month').sum()
# months = range(1 ,13)
# print(all_data.head())

# plt.bar(months , result['Sales'])
# plt.xlabel("Month Number")
# plt.ylabel("Sales in USD ($)")
# plt.show()

# city_result = all_data.groupby(['Cities']).sum()
# city = [cities for cities , df in all_data.groupby('Cities')]
# plt.bar(city , city_result['Sales'])
# plt.xticks(city , rotation = 'vertical' , size = 8)
# plt.xlabel("City Name" )
# plt.ylabel("Sales in USD ($)")
# plt.show()

all_data['Order Date'] = pa.to_datetime(all_data['Order Date'], format='%m/%d/%y %H:%M')
all_data['Hours'] = all_data['Order Date'].dt.hour
all_data['Minutes'] = all_data['Order Date'].dt.minute

Hour = [Hours for Hours , df in all_data.groupby('Hours')] #print(all_data.groupby('Hours').count()['Quantity Ordered']) what the y label doing here is
# plt.plot(Hour , all_data.groupby('Hours').count())
# plt.xticks(Hour)
# plt.grid()
# plt.xlabel("Hours")
# plt.ylabel("Number of Orders")
# plt.show()

# What products are more often sell together?
product_together = all_data[all_data['Order Date'].duplicated(keep = False)].copy()
product_together['Grouped'] = product_together.groupby('Order ID')['Product'].transform(lambda x : ','.join(x))

product_together = product_together[['Order ID' , 'Grouped']].drop_duplicates()
# print(product_together)

from itertools import combinations
from collections import Counter

# Split product groups into pairs
# pair_count = Counter()

# for group in product_together['Grouped']:
#     products = group.split(',')
#     pair_count.update(combinations(products, 2))  # Generate all possible pairs

# # Find the most common pairs
# most_common_pairs = pair_count.most_common(5)  # Top 5 most common pairs

# # Print the result
# for pair, count in most_common_pairs:
#     print(f"Pair: {pair}, Count: {count}")


# Group by 'Product' and sum numeric columns
product_group = all_data.groupby('Product')
quantity_ordered = product_group['Quantity Ordered'].sum()  # Extract only the desired column

# Create a list of products (x-axis labels)
product = [Product for Product in product_group.groups.keys()]  # Use group keys directly

# Plot the bar chart
plt.bar(product, quantity_ordered)
plt.xlabel('Product')
plt.ylabel('Quantity Ordered')
plt.title('Total Quantity Ordered per Product')
plt.xticks(rotation=90)  # Rotate x-axis labels for better visibility

all_data['Price Each'] = pa.to_numeric(all_data['Price Each'], errors='coerce')

# Perform the groupby and mean calculation
prices = all_data.groupby('Product')['Price Each'].mean()

fig , ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.bar(product , quantity_ordered  , color = 'g')
ax2.plot(product , prices , 'b-')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered' , color = 'g')
ax2.set_ylabel('Price {$}' , color = 'b')
ax1.set_xticklabels(product , rotation =90 , size = 8)

plt.show()