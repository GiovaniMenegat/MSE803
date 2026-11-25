import pandas as pd
sales = pd.DataFrame({
	"month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
	"sales": [80000, 85000, 82000, 95000, 110000, 130000],
	"products_sold": [400, 410, 400, 450, 500, 560]
})
# Calculate average sales
average = sales["sales"].mean()
# Find the lowest sales value
lowest_sales = sales["sales"].min()
# Sum of sales
sum_sales = sales["sales"].sum()
# Average sale price of a product for each month (sales in $ / products sold)
sales["avg_sale_price"] = (sales["sales"]) / sales["products_sold"]


# print("Average sales ($):", average)
print("Lowest sales ($):", lowest_sales)
print("Sum of sales ($):", sum_sales)
print("Average sale price per product ($) for each month:")
print(sales[["month", "avg_sale_price"]].to_string(index=False))
