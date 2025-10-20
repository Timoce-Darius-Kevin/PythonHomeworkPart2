'''
Exercise 1

Using pandas, determine the following for the sales.csv data:
The total revenue for each product (quantity  x price_per_unit).
The total cost for each product (quantity  x cost_per_unit).
The profit for each product (total revenue - total cost).
Finally, find the most profitable product overall.
'''
import pandas as pd

sales = pd.read_csv('sales.csv')

sales['total_revenue'] = sales['quantity'] * sales['price_per_unit']
sales['total_cost'] = sales['quantity'] * sales['cost_per_unit']
sales['profit'] = sales['total_revenue'] - sales['total_cost']
most_profitable_product = sales.loc[sales['profit'].idxmax()]
